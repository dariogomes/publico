<?php
class Banco {
	private $db;
	public function __construct(){
		global $config;
		$localhost = $config['host'];
		$user = $config['usuario'];
		$senha = $config['senha'];
		$banco = $config['banco'];
		$connectionInfo =  array( "UID"=>$user, "PWD"=>$senha, "Database"=>$banco);
		try {
			$this->db = new PDO("sqlsrv:server=$localhost;Database = $banco", $user, $senha);  
			$this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		} catch (PDOException $erro) {
			echo $erro->getMessage();
		}

	}
	
	public function select($tabela, $colunas){
		$query = "SELECT $colunas FROM $tabela ORDER BY 1";
		$consulta = $this->db->query($query);
		$dados = $consulta->fetchAll();
		return $dados;
	}

	public function insert($tabela, $dados){
		foreach($dados as $coluna => $valor){
			$colunas[] = $coluna;
			$valores[] = "'".$valor."'";
		}
		$colunas = implode(", ", $colunas);
		$valores = implode(", ", $valores);
		$query = "INSERT INTO $tabela ($colunas) VALUES ($valores)";

		$this->db->exec($query);
	}
	
	public function delete($tabela, $criterio) {
		$query = "DELETE FROM $tabela WHERE $criterio";
        $this->db->exec($query);
    }

	public function truncate($tabela) {
        $query = "TRUNCATE TABLE $tabela";
        $this->db->exec($query);
	}
    
	public function update($tabela, $dados, $where) {
        foreach ($dados as $coluna => $valor) {
            $campos[] = "$coluna = '$valor'";
        }
        $campos = implode(", ", $campos);
		
		foreach ($where as $coluna => $valor) {
            $criterios[] = "$coluna = '$valor'";
        }
		$criterios = implode(" and ", $criterios);
		
        $query = "UPDATE $tabela SET $campos WHERE $criterios";

        $this->db->exec($query);
	}

	public function update2($tabela, $dados, $where) {
        foreach ($dados as $coluna => $valor) {
            $campos[] = "$coluna = '$valor'";
        }
        $campos = implode(", ", $campos);
		
        $query = "UPDATE $tabela SET $campos WHERE $where";
        $this->db->exec($query);
	}


    public function ExecProc($proc) {
        $query = "EXECUTE $proc";
        $this->db->exec($query);
    }

	public function select($tabela, $colunas, $criterios, $order){
		if(empty($criterios)){
			$query = "SELECT $colunas FROM $tabela ORDER BY $order";
		} else {
			$query = "SELECT $colunas FROM $tabela WHERE $criterios ORDER BY $order";
		}
		$consulta = $this->db->query($query);
		$dados = $consulta->fetchAll();
		return $dados;	
	}

	public function SqlSelect($QuerySql){
		$query = "$QuerySql";
		$consulta = $this->db->query($query);
		$dados = $consulta->fetchAll();
		return $dados;
	}

}

?>