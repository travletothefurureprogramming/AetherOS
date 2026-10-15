import json
import os
import questionary

DB_FILE = "cfg/devices.json"


def load_devices():
  if not os.path.exists(DB_FILE):
    return []
  with open(DB_FILE, "r", encoding="utf-8") as f:
    try:
      return json.load(f)
    except json.JSONDecodeError:
      return []


def save_device(device_data):
  devices = load_devices()
  devices.append(device_data)
  with open(DB_FILE, "w", encoding="utf-8") as f:
    json.dump(devices, f, indent=4, ensure_ascii=False)


def main():
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

      if device_type == "💡 Light":
        brand = questionary.select(
            "Select brand:",
            choices=["Tapo", "Tuya", "Yeelight"],
            style=questionary.Style([
                ("pointer", "fg:cyan bold"),
                ("highlighted", "fg:cyan bold"),
            ]),
        ).ask()

        if brand == "Tapo":
          model = questionary.select(
              "Select Tapo model:",
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
              style=questionary.Style([
                  ("pointer", "fg:cyan bold"),
                  ("highlighted", "fg:cyan bold"),
              ]),
          ).ask()

          device_id = questionary.text(
              "Enter unique Device ID (e.g. living_room_light):"
          ).ask()
          ip_address = questionary.text(
              "Enter Device IP Address (e.g. 192.168.1.50):"
          ).ask()

          if device_id and ip_address:
            new_device = {
                "device_id": device_id,
                "device_type": model,
                "brand": brand,
                "ip_address": ip_address,
            }
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
          print(
              f"• ID: {d['device_id']} | Type: {d['device_type']} | IP:"
              f" {d['ip_address']}"
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