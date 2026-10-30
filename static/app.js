body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(180deg, #08181f 0%, #0d1d27 100%);
  color: #ecf5ff;
}

.page-shell {
  max-width: 960px;
  margin: 48px auto;
  padding: 20px;
}

.topbar {
  margin-bottom: 20px;
}

.eyebrow {
  letter-spacing: 0.12em;
  text-transform: uppercase;
  font-size: 12px;
  color: #7bc5ff;
  margin: 0;
}

h1 {
  margin: 8px 0 0;
  font-size: 42px;
}

.panel {
  background: #12242d;
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  padding: 28px;
}

.field {
  display: flex;
  flex-direction: column;
  margin-bottom: 18px;
  gap: 8px;
}

.field span {
  font-weight: 600;
}

input, select, button {
  border-radius: 12px;
  border: 1px solid #2c5164;
  background: #0a1a22;
  color: #ecf5ff;
  padding: 12px 14px;
  font-size: 16px;
}

button {
  background: linear-gradient(135deg, #1b8ae8 0%, #44d7b6 100%);
  border: none;
  cursor: pointer;
  font-weight: 700;
  min-height: 48px;
}

.row {
  display: flex;
  gap: 16px;
}

.two-col > * {
  flex: 1;
}

.summary {
  margin-top: 24px;
  background: #0d1c25;
  border: 1px solid #2d5568;
  border-radius: 16px;
  padding: 20px;
}

.hidden {
  display: none;
}

.summary h2 {
  margin-top: 0;
}

ul {
  padding-left: 20px;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
}

