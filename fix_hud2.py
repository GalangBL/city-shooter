import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# HUD lama: baris 1377-1449 (0-indexed: 1376-1448)
# Baris 1377 dimulai "      // HUD"
# Baris 1449 diakhiri "        );\n      }\n"

# Verifikasi
print("Line 1377:", repr(lines[1376]))
print("Line 1449:", repr(lines[1448]))
print("Line 1450:", repr(lines[1449]))

new_hud_lines = '''      // ====== HUD REDESIGN ======
      const hudFont = "'Orbitron', monospace";
      const hudH = 52;

      // Panel HUD atas semi-transparan
      X.fillStyle = "rgba(0,0,0,0.7)";
      X.fillRect(0, 0, 800, hudH);
      X.strokeStyle = "rgba(255,136,0,0.35)";
      X.lineWidth = 1;
      X.beginPath(); X.moveTo(0, hudH); X.lineTo(800, hudH); X.stroke();

      // === KIRI: HP BAR ===
      X.fillStyle = "#ff8800";
      X.font = "bold 9px " + hudFont;
      X.fillText("HEALTH", 10, 14);
      const hpR = P.hp / P.maxHp;
      const hpColor = hpR > 0.5 ? "#00e060" : hpR > 0.25 ? "#ffaa00" : "#ff2222";
      // Glow saat HP rendah
      if (hpR <= 0.25) { X.shadowColor = "#ff0000"; X.shadowBlur = 8; }
      X.fillStyle = "rgba(255,255,255,0.07)";
      X.fillRect(10, 18, 160, 16);
      X.fillStyle = hpColor;
      X.fillRect(10, 18, 160 * hpR, 16);
      // Segmen HP bar
      for (let s = 1; s < P.maxHp; s++) {
        X.fillStyle = "rgba(0,0,0,0.4)";
        X.fillRect(10 + (160/P.maxHp)*s - 0.5, 18, 1, 16);
      }
      X.strokeStyle = "rgba(255,255,255,0.25)"; X.lineWidth = 1;
      X.strokeRect(10, 18, 160, 16);
      X.shadowBlur = 0;
      X.fillStyle = "#fff"; X.font = "bold 9px " + hudFont;
      X.fillText(P.hp + " / " + P.maxHp, 14, 30);

      // === TENGAH: STAGE + TIMER + SCORE ===
      X.textAlign = "center";
      // Stage badge
      X.fillStyle = "rgba(255,136,0,0.15)";
      X.strokeStyle = "#ff8800"; X.lineWidth = 1;
      X.fillRect(320, 4, 80, 16);
      X.strokeRect(320, 4, 80, 16);
      X.fillStyle = "#ff8800"; X.font = "bold 9px " + hudFont;
      X.fillText("STAGE  " + currentLevel, 360, 16);

      // Timer countdown - BESAR
      const tLeft = Math.max(0, LEVEL_CFG[currentLevel].timeLimit - levelTimer);
      const tMin = Math.floor(tLeft / 60);
      const tSec = Math.floor(tLeft % 60);
      const tStr = tMin + ":" + String(tSec).padStart(2,"0");
      const isUrgent = tLeft < 20;
      if (isUrgent) {
        X.shadowColor = "#ff0000";
        X.shadowBlur = 14;
        X.fillStyle = (Math.floor(Date.now()/250)%2===0) ? "#ff3333" : "#ff9999";
      } else if (tLeft < 40) {
        X.fillStyle = "#ffaa00";
      } else {
        X.fillStyle = "#ffffff";
      }
      X.font = "900 26px " + hudFont;
      X.fillText(tStr, 400, 44);
      X.shadowBlur = 0;

      // Ikon jam kecil
      X.fillStyle = isUrgent ? "#ff4444" : "#aaa";
      X.font = "12px monospace";
      X.fillText("\u23f1", 375, 44);

      // Score
      X.textAlign = "right";
      X.fillStyle = "#888"; X.font = "bold 9px " + hudFont;
      X.fillText("SCORE", 790, 14);
      X.fillStyle = "#ffdd00"; X.font = "bold 18px " + hudFont;
      X.fillText(score, 790, 34);

      // === KANAN: AMMO ICONS ===
      X.textAlign = "left";
      X.fillStyle = "#888"; X.font = "bold 9px " + hudFont;
      const ammoLabelX = 615;
      X.fillText("AMMO", ammoLabelX, 14);
      for (let i = 0; i < P.maxAmmo; i++) {
        const bx = ammoLabelX + i * 19;
        const filled = i < P.ammo;
        if (P.reloading) {
          // Efek reload: isi dari kiri berdasarkan timer
          const reloadFull = P.reloadTimer / 0.8;
          const fillPct = Math.min(1, (reloadFull * P.maxAmmo - i));
          X.fillStyle = fillPct > 0 ? "rgba(255,220,0," + Math.min(1,fillPct) + ")" : "rgba(255,255,255,0.12)";
        } else {
          X.fillStyle = filled ? "#ffdd00" : "rgba(255,255,255,0.12)";
        }
        // Gambar peluru (lonjong)
        X.beginPath();
        X.roundRect(bx, 18, 13, 24, 3);
        X.fill();
        // Highlight
        if (filled && !P.reloading) {
          X.fillStyle = "rgba(255,255,255,0.25)";
          X.fillRect(bx+2, 20, 3, 9);
        }
      }
      if (P.reloading) {
        X.fillStyle = "#ff8800"; X.font = "bold 9px " + hudFont;
        X.fillText("RELOADING...", ammoLabelX, 50);
      }

      // === BOSS HP BAR (Level 3) ===
      if (currentLevel === 3 && enemies.length > 0 && !enemies[0].dead) {
        const boss = enemies[0];
        const bossMaxHp = LEVEL_CFG[3].enemyHp;
        const bossHpR = boss.hp / bossMaxHp;
        X.textAlign = "center";
        // Panel
        X.fillStyle = "rgba(0,0,0,0.7)";
        X.fillRect(140, hudH+4, 520, 24);
        X.strokeStyle = "#ff4400"; X.lineWidth = 1;
        X.strokeRect(140, hudH+4, 520, 24);
        // Bar
        const bc = bossHpR > 0.5 ? "#ff4400" : bossHpR > 0.25 ? "#ff8800" : "#ff0000";
        X.fillStyle = bc;
        X.fillRect(142, hudH+6, 516 * bossHpR, 20);
        X.fillStyle = "#fff"; X.font = "bold 10px " + hudFont;
        X.fillText("\u26A0 BOSS  " + boss.hp + " / " + bossMaxHp + "  \u26A0", 400, hudH+20);
        X.textAlign = "left";
      }

      // === BOTTOM: Kill counter (Level 1 & 2) ===
      if (currentLevel < 3) {
        const killed = Math.floor(score / 10);
        const total = cfg.maxEnemies;
        const remaining = Math.max(0, total - killed);
        X.fillStyle = "rgba(0,0,0,0.6)";
        X.fillRect(0, 374, 190, 26);
        X.fillStyle = remaining > 0 ? "#ff8800" : "#00e060";
        X.font = "bold 10px " + hudFont;
        X.fillText("\u2620 MUSUH: " + remaining + " / " + total, 10, 390);
        // Kill progress bar
        X.fillStyle = "rgba(255,255,255,0.08)";
        X.fillRect(10, 394, 150, 4);
        X.fillStyle = "#ff4400";
        X.fillRect(10, 394, 150 * (killed/total), 4);
      }

'''

# Replace baris 1377-1449 (0-indexed 1376-1449, end exclusive = 1449)
# Line 1449 = "        );\n", line 1450 = "      }\n"  (baris setelah HUD)
new_lines = lines[:1376] + [new_hud_lines] + lines[1449:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("HUD replaced! Total lines:", len(new_lines))
