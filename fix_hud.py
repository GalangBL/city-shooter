import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

ok = []

# ===== 1. Tambah Google Font Orbitron di <head> =====
old1 = '  <meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no" />\n  <title>City Shooter</title>'
new1 = '  <meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no" />\n  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&display=swap" rel="stylesheet">\n  <title>City Shooter</title>'
if old1 in c: c = c.replace(old1, new1); ok.append('1-font')

# ===== 2. Tambah timeLimit ke LEVEL_CFG =====
old2a = '          label: "LEVEL 1 COMPLETE!",'
new2a = '          label: "LEVEL 1 COMPLETE!",\n          timeLimit: 120,'
if old2a in c: c = c.replace(old2a, new2a); ok.append('2a-L1time')

old2b = '          label: "LEVEL 2 COMPLETE!",'
new2b = '          label: "LEVEL 2 COMPLETE!",\n          timeLimit: 90,'
if old2b in c: c = c.replace(old2b, new2b); ok.append('2b-L2time')

old2c = '          label: "BOSS DEFEATED! YOU WIN!",'
new2c = '          label: "BOSS DEFEATED! YOU WIN!",\n          timeLimit: 120,'
if old2c in c: c = c.replace(old2c, new2c); ok.append('2c-L3time')

# ===== 3. Tambah variabel levelTimer ke GAME STATE =====
old3 = '      let transitionTimer = 0;\n      let transitionNextLevel = 1;'
new3 = '      let transitionTimer = 0;\n      let transitionNextLevel = 1;\n      let levelTimer = 0; // countdown timer per level'
if old3 in c: c = c.replace(old3, new3); ok.append('3-timerVar')

# ===== 4. Reset levelTimer di resetLevel() =====
old4 = '        score = 0;\n        spawnTimer = 0;'
new4 = '        score = 0;\n        spawnTimer = 0;\n        levelTimer = 0;'
if old4 in c: c = c.replace(old4, new4); ok.append('4-resetTimer')

# ===== 5. Update timer di upd() setelah updateEnemies =====
old5 = '      // Update hit flash timer\n      if (P.hitFlash > 0) P.hitFlash -= dt;\n\n      updateEnemies(dt);\n    }'
new5 = '''      // Update hit flash timer
      if (P.hitFlash > 0) P.hitFlash -= dt;

      // Countdown timer
      if (!P.dead) {
        levelTimer += dt;
        const tLimit = LEVEL_CFG[currentLevel].timeLimit;
        if (levelTimer >= tLimit) {
          P.dead = true;
          P.deathTimer = 99; // langsung game over
          gamePhase = "gameover";
        }
      }

      updateEnemies(dt);
    }'''
if old5 in c: c = c.replace(old5, new5); ok.append('5-timerLogic')

# ===== 6. Redesign HUD - cari dan replace seluruh blok HUD =====
old_hud = '''        // HUD
        const stateStr = P.dead
          ? "DEAD"
          : P.reloading
            ? "RELOAD"
            : P.shooting
              ? "SHOOT"
              : P.crouching
                ? "CROUCH"
                : P.jumping
                  ? "JUMP"
                  : P.running && Math.abs(P.vx) > 10
                    ? "RUN"
                    : Math.abs(P.vx) > 10
                      ? "WALK"
                      : "IDLE";
        X.fillStyle = "#ff8800";
        X.font = "bold 14px monospace";
        X.fillText(
          "LV" +
            currentLevel +
            " | " +
            stateStr +
            " | Ammo: " +
            P.ammo +
            "/" +
            P.maxAmmo +
            " | Score: " +
            score,
          10,
          20,
        );

        X.fillStyle = "#333";
        X.fillRect(10, 30, 150, 12);
        const hpR = P.hp / P.maxHp;
        X.fillStyle =
          hpR > 0.5 ? "#00cc44" : hpR > 0.25 ? "#ffaa00" : "#ff2222";
        X.fillRect(10, 30, 150 * hpR, 12);
        X.strokeStyle = "#fff";
        X.strokeRect(10, 30, 150, 12);
        X.fillStyle = "#fff";
        X.font = "bold 10px monospace";
        X.fillText("HP: " + P.hp + "/" + P.maxHp, 14, 40);

        // HUD Boss HP bar (level 3)
        if (currentLevel === 3 && enemies.length > 0 && !enemies[0].dead) {
          const boss = enemies[0];
          const bossMaxHp = LEVEL_CFG[3].enemyHp;
          const bossHpR = boss.hp / bossMaxHp;
          X.fillStyle = "#111";
          X.fillRect(200, 10, 400, 18);
          X.fillStyle =
            bossHpR > 0.5 ? "#ff4400" : bossHpR > 0.25 ? "#ff8800" : "#ff0000";
          X.fillRect(200, 10, 400 * bossHpR, 18);
          X.strokeStyle = "#ff8800";
          X.strokeRect(200, 10, 400, 18);
          X.fillStyle = "#fff";
          X.font = "bold 11px monospace";
          X.fillText("BOSS HP: " + boss.hp + "/" + bossMaxHp, 345, 23);
        }

        // Musuh tersisa (sembunyikan untuk level 3 boss)
        const maxEn = cfg.maxEnemies;
        X.fillStyle = "#ff8800";
        X.font = "bold 14px monospace";
        if (currentLevel < 3) {
          X.fillText(
            "Musuh tersisa: " + Math.max(0, maxEn - score / 10) + "/" + maxEn,
            10,
            390,
          );
        }'''

new_hud = '''        // ====== HUD REDESIGN ======
        const hudFont = "'Orbitron', monospace";
        const hudH = 52; // tinggi panel HUD atas

        // Panel atas semi-transparan
        X.fillStyle = "rgba(0,0,0,0.65)";
        X.fillRect(0, 0, 800, hudH);
        X.strokeStyle = "rgba(255,136,0,0.4)";
        X.lineWidth = 1;
        X.beginPath(); X.moveTo(0, hudH); X.lineTo(800, hudH); X.stroke();

        // === KIRI: HP ===
        // Label HP
        X.fillStyle = "#ff8800";
        X.font = "bold 10px " + hudFont;
        X.fillText("HP", 10, 16);
        // Bar HP
        const hpR = P.hp / P.maxHp;
        const barW = 160, barH = 14, barX = 10, barY = 20;
        X.fillStyle = "rgba(255,255,255,0.08)";
        X.fillRect(barX, barY, barW, barH);
        const hpColor = hpR > 0.5 ? "#00e060" : hpR > 0.25 ? "#ffaa00" : "#ff2222";
        X.fillStyle = hpColor;
        X.fillRect(barX, barY, barW * hpR, barH);
        X.strokeStyle = "rgba(255,255,255,0.3)";
        X.lineWidth = 1;
        X.strokeRect(barX, barY, barW, barH);
        // Nilai HP
        X.fillStyle = "#fff";
        X.font = "bold 10px " + hudFont;
        X.fillText(P.hp + "/" + P.maxHp, barX + 4, barY + 11);
        // Flash bar HP saat kena tembak
        if (P.hitFlash > 0) {
          X.fillStyle = "rgba(255,0,0," + (P.hitFlash/0.35*0.4) + ")";
          X.fillRect(barX, barY, barW, barH);
        }

        // === TENGAH: LEVEL + TIMER ===
        const tLeft = Math.max(0, LEVEL_CFG[currentLevel].timeLimit - levelTimer);
        const tMin = Math.floor(tLeft / 60);
        const tSec = Math.floor(tLeft % 60);
        const tStr = tMin + ":" + String(tSec).padStart(2,"0");
        const timerColor = tLeft < 20 ? (Math.floor(Date.now()/300)%2===0 ? "#ff2222" : "#ff8888") : "#ffffff";

        // Level badge
        X.fillStyle = "rgba(255,136,0,0.2)";
        X.fillRect(310, 6, 80, 20);
        X.strokeStyle = "#ff8800"; X.lineWidth = 1;
        X.strokeRect(310, 6, 80, 20);
        X.fillStyle = "#ff8800";
        X.font = "bold 11px " + hudFont;
        X.textAlign = "center";
        X.fillText("STAGE " + currentLevel, 350, 20);

        // Timer besar
        X.font = "bold 22px " + hudFont;
        X.fillStyle = timerColor;
        if (tLeft < 20) { X.shadowColor = "#ff0000"; X.shadowBlur = 10; }
        X.fillText(tStr, 400, 46);
        X.shadowBlur = 0;

        // Score
        X.fillStyle = "#aaa";
        X.font = "bold 10px " + hudFont;
        X.fillText("SCORE", 400, 12);
        X.fillStyle = "#ffdd00";
        X.font = "bold 13px " + hudFont;
        X.fillText(score, 400, 26);
        X.textAlign = "left";

        // === KANAN: AMMO sebagai ikon peluru ===
        const ammoX = 640, ammoY = 8;
        X.fillStyle = "#aaa";
        X.font = "bold 10px " + hudFont;
        X.fillText("AMMO", ammoX, 16);
        // Gambar bullet icons
        for (let i = 0; i < P.maxAmmo; i++) {
          const bx = ammoX + i * 18;
          const filled = i < P.ammo;
          X.fillStyle = filled ? "#ffdd00" : "rgba(255,255,255,0.15)";
          // Bentuk peluru
          X.beginPath();
          X.roundRect(bx, 20, 12, 22, [3, 3, 1, 1]);
          X.fill();
          if (filled) {
            X.fillStyle = "rgba(255,255,255,0.3)";
            X.fillRect(bx+2, 21, 3, 8);
          }
        }
        // Label reload
        if (P.reloading) {
          const reloadPct = P.reloadTimer / 0.8;
          X.fillStyle = "#ff8800";
          X.font = "bold 10px " + hudFont;
          X.fillText("RELOADING...", ammoX, 50);
          X.fillStyle = "rgba(255,136,0,0.3)";
          X.fillRect(ammoX, 52, 144 * reloadPct, 4);
        }

        // === BOSS HP BAR (level 3, full width di atas) ===
        if (currentLevel === 3 && enemies.length > 0 && !enemies[0].dead) {
          const boss = enemies[0];
          const bossMaxHp = LEVEL_CFG[3].enemyHp;
          const bossHpR = boss.hp / bossMaxHp;
          const bossBarY = hudH + 6;
          // Label
          X.textAlign = "center";
          X.fillStyle = "#ff8800";
          X.font = "bold 11px " + hudFont;
          X.fillText("⚠ BOSS", 400, bossBarY + 10);
          // Bar
          X.fillStyle = "rgba(0,0,0,0.6)";
          X.fillRect(80, bossBarY + 14, 640, 12);
          const bc = bossHpR > 0.5 ? "#ff4400" : bossHpR > 0.25 ? "#ff8800" : "#ff0000";
          X.fillStyle = bc;
          X.fillRect(80, bossBarY + 14, 640 * bossHpR, 12);
          X.strokeStyle = "#ff8800"; X.lineWidth = 1;
          X.strokeRect(80, bossBarY + 14, 640, 12);
          X.fillStyle = "#fff";
          X.font = "bold 9px " + hudFont;
          X.fillText(boss.hp + " / " + bossMaxHp, 400, bossBarY + 24);
          X.textAlign = "left";
        }

        // === BOTTOM: Enemy counter (level 1 & 2) ===
        if (currentLevel < 3) {
          const killed = Math.floor(score / 10);
          const total = cfg.maxEnemies;
          const remaining = Math.max(0, total - killed);
          // Panel bawah kiri
          X.fillStyle = "rgba(0,0,0,0.55)";
          X.fillRect(0, 372, 200, 28);
          X.fillStyle = "#ff8800";
          X.font = "bold 10px " + hudFont;
          X.fillText(`MUSUH: ${remaining} / ${total}`, 10, 388);
          // Mini progress bar
          const progW = 140;
          X.fillStyle = "rgba(255,255,255,0.1)";
          X.fillRect(10, 390, progW, 5);
          X.fillStyle = "#ff4400";
          X.fillRect(10, 390, progW * (killed/total), 5);
        }'''

if old_hud in c:
    c = c.replace(old_hud, new_hud); ok.append('6-HUD')
else:
    print("HUD not found - searching fragments...")
    print("'// HUD' found:", '// HUD' in c)
    print("'stateStr' found:", 'stateStr' in c)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied:", ok)
print("Total fixes:", len(ok))
