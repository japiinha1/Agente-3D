<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Agente 3D Pro</title>
    <link rel="stylesheet" href="/static/styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="topbar">
        <div class="brand-block">
          <p class="eyebrow">3D PRINT PRE-FLIGHT</p>
          <h1>Agente 3D Pro</h1>
        </div>
      </header>

      <main class="panel">
        <form id="upload-form" enctype="multipart/form-data">
          <label class="field">
            <span>Arquivo STL / OBJ / 3MF</span>
            <input type="file" name="file" id="file" required />
          </label>

          <div class="row two-col">
            <label class="field">
              <span>Material</span>
              <select name="material" id="material">
                <option>PLA</option>
                <option>PETG</option>
                <option>ABS</option>
                <option>ASA</option>
              </select>
            </label>

            <label class="field">
              <span>Nozzle (mm)</span>
              <input type="number" name="nozzle_mm" id="nozzle_mm" value="0.4" step="0.1" min="0.2" max="0.8" />
            </label>
          </div>

          <div class="row two-col">
            <label class="field">
              <span>Perfil</span>
              <select name="profile_name" id="profile_name">
                <option>Bambu X1C</option>
                <option>Bambu P1S</option>
                <option>Bambu A1</option>
              </select>
            </label>

            <button type="submit">Validar e preparar</button>
          </div>
        </form>

        <section class="preview-panel">
          <div id="preview-container"></div>
        </section>

        <section id="summary" class="summary hidden"></section>
      </main>
    </div>

    <script type="module" src="/static/app.js"></script>
  </body>
</html>

