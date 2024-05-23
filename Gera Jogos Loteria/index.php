<?php

if ($_POST){

  $numeros = $_POST['numeros'];
  $num_end = $_POST['num_end'];
  $tt_jogos = $_POST['tt_jogos'];

  $jogos = array();
  for ($i = 1; $i <= $tt_jogos; $i++)
  {
      $jogo = array();
      for ($e = 1; $e <= $numeros; $e++)
      {
        $rand = rand(1, $num_end);

        if (!in_array($rand, $jogo)){
          //$jogo[] = $rand;
          array_push($jogo, $rand);
        } else {
          $e--;
        }
      }

      sort($jogo);
      $jogo_str = implode(", ", $jogo);

      if (!in_array($jogo_str, $jogos)){
        array_push($jogos, $jogo_str);
      }
  }

  sort($jogos);
} else {
  $numeros = 6;
  $num_end = 15;
  $tt_jogos = 1;
}
?>
<!DOCTYPE html>
<html lang="pt-br">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Gerardor de jogos para loteria</title>

    <!-- Bootstrap -->
    <!-- Última versão CSS compilada e minificada -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- HTML5 shim e Respond.js para suporte no IE8 de elementos HTML5 e media queries -->
    <!-- ALERTA: Respond.js não funciona se você visualizar uma página file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container">
      <form method="POST" action="index.php">
        <div class="form-group">
          <label for="numeros">Quantidade de numero por jogo</label>
          <input type="number" name="numeros" min="1" class="form-control" id="numeros" placeholder="Números por jogo" value="<?php echo $numeros; ?>">
          <p class="help-block text-muted">Informe apenas a quantidade de número que deve conter cada jogo.</p>
        </div>
        <div class="form-group">
          <label for="number">Range de números por jogos</label>
          <input type="number" name="num_end" class="form-control" id="num_end" placeholder="Range de numeros a serem escolhidos por jogo" value="<?php echo $num_end; ?>">
          <p class="help-block text-muted">Informe a range de números que devem ser escolhidos em cada jogo.</p>
        </div>
        <div class="form-group">
          <label for="number">Quantidade de jogos</label>
          <input type="number" name="tt_jogos" class="form-control" id="tt_jogos" placeholder="Quantidade de jogos a serem gerados" value="<?php echo $tt_jogos; ?>">
          <p class="help-block text-muted">Informe a quantidade de jogos que deseja.</p>
        </div>
        <button type="submit" class="btn btn-primary">Gerar jogos</button>
      </form>
    </div>
    <div class="container">
      <?php
      if (isset($jogos)){
        echo "<h1>Jogos!</h1>";
        echo "<table class='table table-striped table-condensed table-hover'>";
          $x = 1;
          foreach ($jogos as $dado)
          {
            echo "<tr>";
            echo "<td>Jogo ".$x.": </td><td>".$dado."</td>";
            echo "</tr>";
            $x++;
          }
        echo "</table>";
      }
      ?>
    </div>
    <!-- jQuery (obrigatório para plugins JavaScript do Bootstrap) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Inclui todos os plugins compilados (abaixo), ou inclua arquivos separadados se necessário -->
    <!-- Última versão JavaScript compilada e minificada -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
  </body>
</html>
