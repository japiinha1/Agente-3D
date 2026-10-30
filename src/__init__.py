* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(180deg, #07151d 0%, #102330 100%);
  color: #edf8ff;
}

.page-shell {
  max-width: 1080px;
  margin: 48px auto;
  padding: 20px;
}

.topbar {
  margin-bottom: 24px;
}

.brand-block {
  padding: 20px 0;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
  color: #7bd0ff;
}

h1 {
  margin: 10px 0 0;
  font-size: clamp(32px, 4vw, 52px);
}

.panel {
  background: rgba(18, 35, 44, 0.94);
  border: 1px solid rgba(123, 208, 255, 0.2);
  border-radius: 18px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
  padding: 28px;
}

.field {
  display: flex;
  flex-direction: column;
  margin-bottom: 18px;
  gap: 8px;
}

.field span {
  font-weight: 700;
  color: #dfefff;
}

input, select, button {
  width: 100%;
  border-radius: 12px;
  border: 1px solid #2d586b;
  background: #0d1a22;
  color: #edf8ff;
  padding: 12px 14px;
  font-size: 16px;
}

button {
  background: linear-gradient(135deg, #1d91ff 0%, #48dbb6 100%);
  border: none;
  cursor: pointer;
  font-weight: 800;
  color: #07151d;
  min-height: 52px;
}

.row {
  display: flex;
  gap: 16px;
}

.two-col > * {
  flex: 1;
}

.preview-panel {
  margin-top: 18px;
  margin-bottom: 18px;
  background: rgba(8, 18, 24, 0.9);
  border: 1px solid rgba(123, 208, 255, 0.2);
  border-radius: 18px;
  overflow: hidden;
  min-height: 360px;
}

#preview-container {
  width: 100%;
  min-height: 360px;
}

#preview-container canvas {
  display: block;
  width: 100%;
  height: 360px;
}

.summary {
  margin-top: 24px;
  background: rgba(8, 17, 22, 0.92);
  border: 1px solid rgba(123, 208, 255, 0.22);
  border-radius: 16px;
  padding: 20px;
}

.hidden {
  display: none;
}

h2, h3 {
  margin-top: 0;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.badge {
  display: inline-block;
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.badge.ready_for_review {
  background: rgba(72, 219, 182, 0.18);
  color: #8af0d8;
}

.badge.review_required {
  background: rgba(255, 182, 71, 0.18);
  color: #ffc76b;
}

.badge.needs_repair {
  background: rgba(255, 93, 93, 0.18);
  color: #ff9e9e;
}

.score {
  font-weight: 700;
  color: #b8e6ff;
}

ul {
  padding-left: 20px;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 14px;
}

@media (max-width: 640px) {
  .row {
    flex-direction: column;
  }
}

