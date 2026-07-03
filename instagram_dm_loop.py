from instagrapi import Client
import time
import random
import os
import sys

cl = Client()

USERNAME = ""
PASSWORD = ""
targets = []
MESSAGE = "Salut! Ce mai faci? 😊"
DELAY_MIN = 60
DELAY_MAX = 120

def clear():
    os.system('clear')

def load_targets():
    global targets
    print("\n📂 Fișiere .txt din folderul curent:")
    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")
    if not files:
        print("❌ Nu ai niciun fișier .txt!")
        return False
    choice = input("\nAlege numărul fișierului: ")
    try:
        file_name = files[int(choice)-1]
        with open(file_name, 'r', encoding='utf-8') as f:
            targets = [line.strip() for line in f if line.strip()]
        print(f"✅ S-au încărcat {len(targets)} usernames din {file_name}")
        return True
    except:
        print("❌ Eroare la citirea fișierului!")
        return False

def login():
    global USERNAME, PASSWORD
    USERNAME = input("📧 Username Instagram: ")
    PASSWORD = input("🔑 Parola: ")
    try:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings("session.json")
        print("✅ Login reușit!")
        return True
    except Exception as e:
        print(f"❌ Login eșuat: {e}")
        return False

def settings_menu():
    global MESSAGE, DELAY_MIN, DELAY_MAX
    while True:
        clear()
        print("╔════════════════════════════════════╗")
        print("║       INSTAGRAM DM LOOP MENU       ║")
        print("╠════════════════════════════════════╣")
        print(f"║ 1. Mesaj → {MESSAGE[:40]}...     ║")
        print(f"║ 2. Delay min → {DELAY_MIN}s          ║")
        print(f"║ 3. Delay max → {DELAY_MAX}s          ║")
        print("║ 4. Schimbă fișier targets          ║")
        print("║ 5. Start Loop Infinit              ║")
        print("║ 6. Ieșire                          ║")
        print("╚════════════════════════════════════╝")
        
        opt = input("\nAlege opțiunea: ")
        
        if opt == "1":
            MESSAGE = input("Scrie noul mesaj:\n")
        elif opt == "2":
            DELAY_MIN = int(input("Delay minim (secunde): "))
        elif opt == "3":
            DELAY_MAX = int(input("Delay maxim (secunde): "))
        elif opt == "4":
            load_targets()
        elif opt == "5":
            if not targets:
                print("❌ Încarcă mai întâi un fișier cu usernames!")
                input("\nApasă Enter...")
                continue
            start_loop()
        elif opt == "6":
            print("La revedere!")
            sys.exit()

def start_loop():
    print(f"\n🚀 START LOOP INFINIT - {len(targets)} conturi")
    print("Pentru a opri: Ctrl + C\n")
    sent = 0
    while True:
        for user in targets:
            try:
                uid = cl.user_id_from_username(user)
                cl.direct_send(MESSAGE, [uid])
                sent += 1
                print(f"✅ [{sent}] Trimis către @{user}")
            except Exception as e:
                print(f"❌ Eroare @{user} | {e}")
            
            timp = random.randint(DELAY_MIN, DELAY_MAX)
            print(f"⏳ Aștept {timp} secunde...")
            time.sleep(timp)

clear()
print("🌟 Instagram DM Automat - Loop Infinit\n")

if os.path.exists("session.json"):
    try:
        cl.load_settings("session.json")
        print("✅ Sesiune încărcată!")
    except:
        login()
else:
    login()

load_targets()
settings_menu()