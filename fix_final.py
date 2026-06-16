import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

ok = []

# 1. timeLimit di Level 1
old1 = '          label: "LEVEL 1 COMPLETE!",'
new1 = '          label: "LEVEL 1 COMPLETE!",\n          timeLimit: 120,'
if old1 in c: c = c.replace(old1, new1); ok.append('L1-time')

# 2. timeLimit di Level 2
old2 = '          label: "LEVEL 2 COMPLETE!",'
new2 = '          label: "LEVEL 2 COMPLETE!",\n          timeLimit: 90,'
if old2 in c: c = c.replace(old2, new2); ok.append('L2-time')

# 3. timeLimit di Level 3 Boss
old3 = '          label: "BOSS DEFEATED! YOU WIN!",'
new3 = '          label: "BOSS DEFEATED! YOU WIN!",\n          timeLimit: 120,'
if old3 in c: c = c.replace(old3, new3); ok.append('L3-time')

# 4. reset levelTimer di resetLevel
old4 = '        score = 0;\n        spawnTimer = 0;\n        totalSpawned = 0;\n        enemies = [];\n        enemyBullets = [];\n        bullets = [];\n        particles = [];\n        resetPlayer();\n        cameraX = 0;'
new4 = '        score = 0;\n        spawnTimer = 0;\n        totalSpawned = 0;\n        enemies = [];\n        enemyBullets = [];\n        bullets = [];\n        particles = [];\n        levelTimer = 0;\n        resetPlayer();\n        cameraX = 0;'
if old4 in c: c = c.replace(old4, new4); ok.append('resetTimer')
else:
    # Coba variasi
    idx = c.find('resetPlayer()')
    if idx > 0:
        print("resetPlayer found at:", idx)
        print(repr(c[idx-200:idx+50]))

# 5. Perbaiki Menu screen pakai Orbitron
old5 = '        X.fillStyle = "#ff8800"; X.font = "bold 64px monospace";\n        X.textAlign = "center";\n        X.fillText("CITY SHOOTER", 400, 140);\n        X.shadowBlur = 0;\n\n        X.fillStyle = "#ffffff"; X.font = "18px monospace";\n        X.fillText("3 Level  |  Final Boss  |  Side Scroller", 400, 180);'
new5 = '        X.fillStyle = "#ff8800"; X.font = "900 62px \'Orbitron\', monospace";\n        X.textAlign = "center";\n        X.fillText("CITY SHOOTER", 400, 138);\n        X.shadowBlur = 0;\n\n        X.fillStyle = "#ffdd00"; X.font = "bold 14px \'Orbitron\', monospace";\n        X.fillText("3 STAGE  \u2022  FINAL BOSS  \u2022  SIDE SCROLLER", 400, 172);'
if old5 in c: c = c.replace(old5, new5); ok.append('menu-font')

# 6. Game Over font
old6 = '        X.fillStyle = "#ff2222"; X.font = "bold 72px monospace";\n        X.textAlign = "center";\n        X.fillText("GAME OVER", 400, 160);'
new6 = '        X.fillStyle = "#ff2222"; X.font = "900 68px \'Orbitron\', monospace";\n        X.textAlign = "center";\n        X.fillText("GAME OVER", 400, 162);'
if old6 in c: c = c.replace(old6, new6); ok.append('gameover-font')

# 7. Win screen font
old7 = '        X.fillStyle = "#00ff88"; X.font = "bold 52px monospace";\n        X.textAlign = "center";\n        X.fillText("MISSION COMPLETE!", 400, 130);'
new7 = '        X.fillStyle = "#00ff88"; X.font = "900 44px \'Orbitron\', monospace";\n        X.textAlign = "center";\n        X.fillText("MISSION COMPLETE!", 400, 128);'
if old7 in c: c = c.replace(old7, new7); ok.append('win-font')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied:", ok)
print("Total:", len(ok), "fixes")
