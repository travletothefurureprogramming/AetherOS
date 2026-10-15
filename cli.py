import json
import os
import questionary

CONFIG_DIR = "cfg"
DB_FILE = os.path.join(CONFIG_DIR, "devices.json")


def ensure_config_dir():
  """Δημιουργεί τον φάκελο cfg αν δεν υπάρχει già."""
  if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)


def load_devices():
  if not os.path.exists(DB_FILE):
    return []
  with open(DB_FILE, "r", encoding="utf-8") as f:
    try:
      return json.load(f)
    except json.JSONDecodeError:
      return []


def save_device(device_data):
  ensure_config_dir()
  devices = load_devices()
  devices.append(device_data)
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(devices, f, indent=4, ensure_ascii=False)


def main():
  ensure_config_dir()

  while True:
    os.system("cls" if os.name == "nt" else "clear")

    print("""
    ╔══════════════════════════════════════╗
    ║               AetherOS               ║
    ║       Local-First IoT Hub v1.0       ║
    ╚══════════════════════════════════════╝
    """)

    choice = questionary.select(
        "Select an operation:",
        choices=[
            "🔌 Add / Register New Device",
            "📋 View Registered Devices",
            "🚀 Start API Server",
            "❌ Exit",
        ],
        style=questionary.Style([
            ("pointer", "fg:cyan bold"),
            ("highlighted", "fg:cyan bold"),
        ]),
    ).ask()

    if choice == "🔌 Add / Register New Device":
      device_type = questionary.select(
          "Select device type:",
          choices=["💡 Light", "⚡ Plug", "📺 TV"],
          style=questionary.Style([
              ("pointer", "fg:cyan bold"),
              ("highlighted", "fg:cyan bold"),
          ]),
      ).ask()

      if device_type in ["💡 Light", "⚡ Plug"]:
        brand = questionary.select(
            "Select brand:",
            choices=["Tapo", "Tuya", "Yeelight", "Shelly"],
            style=questionary.Style([
                ("pointer", "fg:cyan bold"),
                ("highlighted", "fg:cyan bold"),
            ]),
        ).ask()

        model = None
        if brand == "Tapo":
          if device_type == "💡 Light":
            model = questionary.select(
                "Select Tapo Light model:",
                choices=[
                    "tapo_l530",
                    "tapo_l535",
                    "tapo_l510",
                    "tapo_l630",
                    "tapo_l610",
                    "tapo_l900",
                    "tapo_l920",
                    "tapo_l930",
                ],
            ).ask()
          elif device_type == "⚡ Plug":
            model = questionary.select(
                "Select Tapo Plug model:",
                choices=["tapo_p100", "tapo_p110", "tapo_p115"],
            ).ask()

        device_id = questionary.text(
            "Enter unique Device ID (e.g. living_room_light):"
        ).ask()
        ip_address = questionary.text(
            "Enter Device IP Address (e.g. 192.168.1.50):"
        ).ask()

        email = None
        password = None
        if brand == "Tapo":
          email = questionary.text("Enter Tapo Account Email:").ask()
          password = questionary.password("Enter Tapo Account Password:").ask()

        if device_id and ip_address:
          new_device = {
              "device_id": device_id,
              "device_type": model or device_type.lower(),
              "brand": brand,
              "ip_address": ip_address,
          }

          if brand == "Tapo":
            new_device["auth"] = {"email": email, "password": password}

          save_device(new_device)
          print(f"\n[✔] Device '{device_id}' successfully registered!")

      input("\nPress Enter to continue...")

    elif choice == "📋 View Registered Devices":
      devices = load_devices()
      print("\n--- Registered Devices ---")
      if not devices:
        print("No devices found.")
      else:
        for d in devices:
          auth_info = " (Auth Configured)" if "auth" in d else ""
          print(
              f"• ID: {d['device_id']} | Brand: {d['brand']} | Type:"
              f" {d['device_type']} | IP: {d['ip_address']}{auth_info}"
          )
      input("\nPress Enter to continue...")

    elif choice == "🚀 Start API Server":
      print("\n[+] Starting API Server...")
      break

    elif choice == "❌ Exit" or choice is None:
      print("\nGoodbye!")
      break


if __name__ == "__main__":
  main()