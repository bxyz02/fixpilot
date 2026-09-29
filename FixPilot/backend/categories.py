"""Data-driven category definitions for the diagnostic hub."""

PC_FEATURES = [
    {"name":"cpu_temp","label":"CPU temperature","type":"number","min":20,"max":110,"unit":"°C","default":55},
    {"name":"gpu_temp","label":"GPU temperature","type":"number","min":20,"max":110,"unit":"°C","default":55},
    {"name":"fan_noise","label":"Fan noise","type":"select","options":["low","normal","high"],"default":"normal"},
    {"name":"overheating","label":"Overheating observed","type":"boolean"},
    {"name":"pc_age","label":"PC age","type":"number","min":0,"max":25,"unit":"years","default":3},
    {"name":"cpu_age","label":"CPU age","type":"number","min":0,"max":25,"unit":"years","default":3},
    {"name":"gpu_age","label":"GPU age","type":"number","min":0,"max":25,"unit":"years","default":3},
    {"name":"ram_capacity","label":"RAM capacity","type":"number","min":2,"max":128,"unit":"GB","default":16},
    {"name":"storage_type","label":"Storage type","type":"select","options":["ssd","hdd","nvme"],"default":"ssd"},
    {"name":"storage_health","label":"Storage health","type":"select","options":["good","fair","poor"],"default":"good"},
    {"name":"os","label":"Operating system","type":"select","options":["win11","win10","win7","linux"],"default":"win11"},
    *[{"name":n,"label":n.replace("_"," ").title(),"type":"number","min":0,"max":100,"unit":"%","default":50} for n in ("cpu_usage","gpu_usage","ram_usage","storage_usage")],
    *[{"name":n,"label":n.replace("_"," ").title(),"type":"boolean"} for n in ("performance_slowdown","random_shutdowns","blue_screen","freezing","crashes","system_restarts","slow_startup","boot_failure","black_screen","screen_artifacts","disk_errors","power_issues","error_messages","recent_driver_update","recent_windows_update","malware_symptoms","internet_problems","wifi_problems")],
    {"name":"dust_level","label":"Dust level","type":"select","options":["low","medium","high"],"default":"medium"},
    {"name":"thermal_paste_age","label":"Thermal paste age","type":"number","min":0,"max":20,"unit":"years","default":2},
    {"name":"last_maintenance","label":"Years since maintenance","type":"number","min":0,"max":20,"unit":"years","default":1},
    {"name":"loud_fans","label":"Loud fans","type":"boolean"},
]

def F(name, label, kind="boolean", **extra):
    return {"name":name,"label":label,"type":kind,**extra}

def spec(slug, name, icon, description, features, labels, signatures, actions):
    return {"id":slug,"name":name,"icon":icon,"description":description,"features":features,
            "labels":labels,"signatures":signatures,"actions":actions,
            "dataset":f"{slug}_diagnosis_dataset.xlsx"}

SPECS = {
"pc": spec("pc","PC / Computer","🖥️","Diagnose hardware, temperatures, memory, storage, Windows, power, boot and network problems.",PC_FEATURES,
 ["CPU overheating","GPU overheating","RAM problem","SSD/HDD problem","Power supply problem","Windows/software problem","Driver problem","Network adapter problem","Motherboard problem","Malware/security problem","Cooling problem","Display/GPU problem","Boot problem","Performance problem","Unknown"],{},{}),
"smartphone": spec("smartphone","Smartphone","📱","Battery, charging, heat, performance, display, camera and connectivity.",[
 F("battery_health","Battery health","number",min=40,max=100,unit="%",default=88),F("drain_rate","Battery drain per hour","number",min=0,max=35,unit="%/h",default=8),F("charge_minutes","Time to charge 20%","number",min=5,max=120,unit="min",default=25),F("temperature","Device temperature","number",min=20,max=70,unit="°C",default=34),F("storage_usage","Storage used","number",min=0,max=100,unit="%",default=60),F("ram_usage","Memory used","number",min=0,max=100,unit="%",default=55),F("charging_failure","Charging fails","boolean"),F("overheating","Overheating","boolean"),F("app_crashes","Apps crash","boolean"),F("screen_issue","Screen/display issue","boolean"),F("touch_issue","Touch input issue","boolean"),F("camera_issue","Camera issue","boolean"),F("network_issue","Wi-Fi or mobile data issue","boolean"),F("unexpected_restarts","Unexpected restarts","boolean")],
 ["Battery degradation","Charging port or cable fault","Thermal stress","Storage pressure","App or OS instability","Display or touch fault","Camera fault","Network fault"],
 {"Battery degradation":["battery_health","drain_rate"],"Charging port or cable fault":["charge_minutes","charging_failure"],"Thermal stress":["temperature","overheating"],"Storage pressure":["storage_usage","ram_usage"],"App or OS instability":["app_crashes","unexpected_restarts"],"Display or touch fault":["screen_issue","touch_issue"],"Camera fault":["camera_issue"],"Network fault":["network_issue"]},
 {"Battery degradation":["Review battery health and replace the battery if service is recommended.","Reduce background activity and screen brightness."],"Charging port or cable fault":["Try a certified cable and charger.","Inspect the port for debris; seek service if it is loose or damaged."],"Thermal stress":["Stop intensive use while hot and remove the case temporarily.","Keep the phone out of direct sun; arrange service if overheating continues."],"Storage pressure":["Remove unused files and apps.","Restart the phone and check storage again."],"App or OS instability":["Update the affected apps and operating system.","Back up data before resetting or seeking service."],"Display or touch fault":["Restart the phone and check for a screen protector obstruction.","Back up data and arrange screen service if the fault persists."],"Camera fault":["Clean the lens and restart the camera app.","Update the system and arrange service if the camera remains unavailable."],"Network fault":["Toggle airplane mode and reset network settings.","Check carrier or router status and install system updates."]}),
"wifi": spec("wifi","Wi-Fi / Internet","📶","Diagnose slow internet, high ping, dropouts, weak signal, DNS and router trouble.",[
 F("download_speed","Download speed","number",min=0,max=1000,unit="Mbps",default=100),F("upload_speed","Upload speed","number",min=0,max=500,unit="Mbps",default=30),F("ping","Ping","number",min=0,max=1000,unit="ms",default=25),F("signal_strength","Wi-Fi signal","number",min=0,max=100,unit="%",default=75),F("connected_devices","Connected devices","number",min=1,max=100,default=8),F("disconnects","Frequent disconnections","boolean"),F("weak_signal","Weak signal","boolean"),F("dns_error","DNS errors","boolean"),F("router_restarts","Router restarts","boolean"),F("all_devices_affected","All devices affected","boolean"),F("wired_slow","Wired connection also slow","boolean"),F("high_latency","High latency or jitter","boolean")],
 ["ISP or line congestion","Weak Wi-Fi coverage","Router instability","DNS configuration fault","Local device adapter fault","Network congestion or interference","High latency route"],
 {"ISP or line congestion":["download_speed","wired_slow","all_devices_affected"],"Weak Wi-Fi coverage":["signal_strength","weak_signal"],"Router instability":["router_restarts","disconnects"],"DNS configuration fault":["dns_error"],"Local device adapter fault":["disconnects","all_devices_affected"],"Network congestion or interference":["connected_devices","download_speed"],"High latency route":["ping","high_latency"]},
 {"ISP or line congestion":["Restart the modem once and compare a wired speed test.","Contact your internet provider with test results."],"Weak Wi-Fi coverage":["Move closer to the router or reposition it in an open central spot.","Use a mesh node or access point for distant rooms."],"Router instability":["Check ventilation and install router firmware updates.","Replace aging power adapters or router hardware if resets continue."],"DNS configuration fault":["Set DNS to your provider's recommended resolver or a trusted public resolver.","Flush device DNS cache and restart the router."],"Local device adapter fault":["Forget and rejoin the network; update the device network driver.","Compare with another device in the same location."],"Network congestion or interference":["Pause heavy downloads and review connected devices.","Use 5 GHz or 6 GHz Wi-Fi and a less congested channel."],"High latency route":["Test by Ethernet and pause background uploads.","Choose a nearby game or service region and contact the provider if persistent."]}),
"gaming": spec("gaming","Gaming / Console","🎮","Diagnose frame drops, crashes, heat, controller, online play and storage.",[
 F("fps_drop","Frame rate drop","boolean"),F("crashes","Game crashes","boolean"),F("temperature","Console or PC temperature","number",min=20,max=110,unit="°C",default=58),F("fan_noise","Fan noise","select",options=["low","normal","high"],default="normal"),F("ping","Online ping","number",min=0,max=1000,unit="ms",default=35),F("disconnects","Online disconnections","boolean"),F("controller_issue","Controller issue","boolean"),F("storage_free","Free storage","number",min=0,max=1000,unit="GB",default=150),F("updates_pending","Updates pending","boolean"),F("artifacts","Visual artifacts","boolean"),F("overheating","Overheating warning","boolean"),F("all_games_affected","All games affected","boolean")],
 ["Thermal throttling","Graphics or performance bottleneck","Game or system software fault","Network connection fault","Controller or input fault","Storage pressure","Display or graphics fault"],
 {"Thermal throttling":["temperature","fan_noise","overheating"],"Graphics or performance bottleneck":["fps_drop","all_games_affected"],"Game or system software fault":["crashes","updates_pending"],"Network connection fault":["ping","disconnects"],"Controller or input fault":["controller_issue"],"Storage pressure":["storage_free"],"Display or graphics fault":["artifacts"]},
 {"Thermal throttling":["Improve ventilation and clear dust from vents.","Stop play if temperatures remain unsafe and arrange service."],"Graphics or performance bottleneck":["Update graphics software and lower demanding settings.","Check whether the issue affects one game or all games."],"Game or system software fault":["Install game and system updates; verify or reinstall the affected game.","Back up saves before resetting system software."],"Network connection fault":["Prefer Ethernet and pause other network traffic.","Check service status and router signal."],"Controller or input fault":["Charge or replace batteries and reconnect the controller.","Update controller firmware and test another controller."],"Storage pressure":["Free storage space and check drive health.","Move games to supported healthy storage."],"Display or graphics fault":["Check display cable and try another screen or port.","Update graphics software and seek service if artifacts persist."]}),
"battery": spec("battery","Battery / Charging","🔋","Diagnose rapid drain, slow charging, heat, charging failures and battery wear.",[
 F("battery_health","Battery health","number",min=30,max=100,unit="%",default=90),F("drain_rate","Drain rate","number",min=0,max=50,unit="%/h",default=7),F("charge_minutes","Time to charge 20%","number",min=5,max=180,unit="min",default=25),F("temperature","Battery temperature","number",min=15,max=80,unit="°C",default=32),F("charging_failure","Charging stops or fails","boolean"),F("charger_wattage","Charger rating","number",min=1,max=300,unit="W",default=30),F("swelling","Battery swelling","boolean"),F("cable_damage","Cable or adapter damage","boolean"),F("device_age","Device age","number",min=0,max=20,unit="years",default=2),F("background_drain","High background usage","boolean")],
 ["Worn battery","Cable or adapter fault","Charging port fault","Thermal charging protection","Battery safety fault","Background power drain","Slow or underpowered charger"],
 {"Worn battery":["battery_health","drain_rate","device_age"],"Cable or adapter fault":["cable_damage","charging_failure"],"Charging port fault":["charging_failure"],"Thermal charging protection":["temperature","charge_minutes"],"Battery safety fault":["swelling"],"Background power drain":["background_drain","drain_rate"],"Slow or underpowered charger":["charger_wattage","charge_minutes"]},
 {"Worn battery":["Check the manufacturer's battery health report.","Replace the battery through a qualified service provider if health is poor."],"Cable or adapter fault":["Use a certified undamaged cable and adapter.","Stop using damaged or unusually hot charging equipment."],"Charging port fault":["Inspect the port for debris without using metal tools.","Arrange professional port service if the connection is loose."],"Thermal charging protection":["Let the device cool at room temperature before charging.","Avoid charging in direct sun or under bedding."],"Battery safety fault":["Stop using and charging the device.","Keep it away from heat and arrange qualified battery service promptly."],"Background power drain":["Review battery usage by app and restrict unnecessary background activity.","Install system updates and restart the device."],"Slow or underpowered charger":["Use a charger that meets the device's recommended power rating.","Try a compatible cable and check charging speed again."]}),
"car": spec("car","Car","🚗","Diagnose starting, battery, engine, temperature, warning lights and braking symptoms.",[
 F("starting_failure","Slow cranking or no start","boolean"),F("battery_voltage","Battery voltage","number",min=8,max=16,unit="V",default=12.5),F("cranking_slow","Slow cranking","boolean"),F("engine_temp","Engine temperature","number",min=40,max=150,unit="°C",default=90),F("warning_light","Warning light on","boolean"),F("check_engine","Check engine light","boolean"),F("brake_noise","Brake noise or vibration","boolean"),F("fluid_leak","Fluid leak","boolean"),F("rough_idle","Rough idle","boolean"),F("smoke","Unusual exhaust smoke","boolean"),F("overheating","Engine overheating","boolean"),F("age_years","Vehicle age","number",min=0,max=40,unit="years",default=7)],
 ["Weak battery or starter","Charging system fault","Engine overheating","Brake system concern","Engine misfire or sensor fault","Fluid leak","Exhaust or combustion issue"],
 {"Weak battery or starter":["battery_voltage","cranking_slow","starting_failure"],"Charging system fault":["battery_voltage","warning_light"],"Engine overheating":["engine_temp","overheating"],"Brake system concern":["brake_noise","warning_light"],"Engine misfire or sensor fault":["rough_idle","check_engine"],"Fluid leak":["fluid_leak"],"Exhaust or combustion issue":["smoke"]},
 {"Weak battery or starter":["Have the battery and starter tested.","Check terminal connections and replace a weak battery."],"Charging system fault":["Have the alternator and charging voltage tested.","Limit driving if the charging warning remains on."],"Engine overheating":["Pull over safely, switch off the engine and let it cool.","Do not open a hot cooling system; arrange inspection before continuing."],"Brake system concern":["Avoid driving if braking feels reduced or a brake warning is present.","Arrange prompt inspection by a qualified mechanic."],"Engine misfire or sensor fault":["Read diagnostic trouble codes with a scan tool.","Arrange service if the engine runs roughly or the warning flashes."],"Fluid leak":["Identify the fluid only when the vehicle is cool and parked safely.","Do not drive with a significant leak; arrange inspection."],"Exhaust or combustion issue":["Avoid prolonged driving if smoke is heavy or the engine loses power.","Arrange an engine and exhaust inspection."]}),
"home_electronics": spec("home_electronics","Home Electronics","🏠","Diagnose TVs, monitors, speakers, printers, routers and other electronics.",[
 F("device_type","Device type","select",options=["tv","monitor","printer","speaker","router","other"],default="tv"),F("power_failure","Won't power on","boolean"),F("intermittent_power","Power cuts out","boolean"),F("display_issue","No or distorted image","boolean"),F("sound_issue","No or distorted sound","boolean"),F("connection_issue","Connection problem","boolean"),F("overheating","Device feels unusually hot","boolean"),F("error_code","Error code shown","boolean"),F("paper_jam","Paper jam or feed issue","boolean"),F("age_years","Device age","number",min=0,max=30,unit="years",default=4),F("cable_changed","Cable recently changed","boolean")],
 ["Power adapter or supply fault","Display panel or cable fault","Audio output fault","Network or pairing fault","Printer feed or paper fault","Firmware or configuration fault","Overheating or blocked ventilation"],
 {"Power adapter or supply fault":["power_failure","intermittent_power"],"Display panel or cable fault":["display_issue","cable_changed"],"Audio output fault":["sound_issue"],"Network or pairing fault":["connection_issue","device_type"],"Printer feed or paper fault":["paper_jam","device_type"],"Firmware or configuration fault":["error_code"],"Overheating or blocked ventilation":["overheating"]},
 {"Power adapter or supply fault":["Try a known compatible power cable and outlet.","Stop using the device if you smell burning or see damage."],"Display panel or cable fault":["Reseat or replace the video cable and check another input.","Arrange panel service if the problem appears on every source."],"Audio output fault":["Check mute, output selection and cable or Bluetooth pairing.","Test another source before arranging speaker service."],"Network or pairing fault":["Restart both devices and renew the network or pairing connection.","Install firmware updates from the manufacturer."],"Printer feed or paper fault":["Remove paper carefully and reload the tray guides.","Clean feed rollers and check the printer error guide."],"Firmware or configuration fault":["Record the error code and check the manufacturer's support guide.","Restart and update firmware using the official utility."],"Overheating or blocked ventilation":["Power off and clear vents; leave space around the device.","Arrange service if it continues to overheat."]}),
"electrical": spec("electrical","Electrical / Power","⚡","Diagnose power interruptions, unstable supply, adapters, cables and shutdowns.",[
 F("outage","Power outage or interruption","boolean"),F("voltage","Measured voltage","number",min=0,max=300,unit="V",default=120),F("voltage_fluctuation","Lights or voltage fluctuate","boolean"),F("breaker_trip","Breaker trips","boolean"),F("adapter_hot","Adapter unusually hot","boolean"),F("cable_damage","Cable damaged","boolean"),F("burning_smell","Burning smell or sparks","boolean"),F("device_shutdown","Device shuts down","boolean"),F("multiple_devices","Multiple devices affected","boolean"),F("surge_recent","Recent surge or storm","boolean"),F("ups_alarm","UPS alarm or fault","boolean")],
 ["Utility supply interruption","Overloaded circuit","Damaged cable or connection","Adapter or power supply fault","Surge damage","UPS or backup fault","Unsafe overheating or arcing"],
 {"Utility supply interruption":["outage","multiple_devices"],"Overloaded circuit":["breaker_trip","multiple_devices"],"Damaged cable or connection":["cable_damage","device_shutdown"],"Adapter or power supply fault":["adapter_hot","device_shutdown"],"Surge damage":["surge_recent","device_shutdown"],"UPS or backup fault":["ups_alarm"],"Unsafe overheating or arcing":["burning_smell","adapter_hot"]},
 {"Utility supply interruption":["Check whether neighboring circuits or utility service are affected.","Contact the utility provider if the supply remains unstable."],"Overloaded circuit":["Unplug nonessential loads and identify recent additions.","Have a qualified electrician inspect repeated breaker trips."],"Damaged cable or connection":["Stop using damaged cables and replace them with correctly rated parts.","Have loose or hot outlets inspected by an electrician."],"Adapter or power supply fault":["Disconnect the hot adapter and replace it with a compatible certified unit.","Check device power requirements before reconnecting."],"Surge damage":["Disconnect affected equipment and inspect for damage.","Use a correctly rated surge protector after the supply is stable."],"UPS or backup fault":["Check the UPS load, battery status and alarm code.","Replace aged batteries with the correct model."],"Unsafe overheating or arcing":["Disconnect power at a safe point if possible and keep clear.","Arrange urgent inspection by a qualified electrician."]}),
}

SEQUENCES = {
    "pc": [
        ("Hardware", "Core components and system age", ["pc_age", "cpu_age", "gpu_age", "ram_capacity"]),
        ("Performance", "Resource usage and slowdown", ["cpu_usage", "gpu_usage", "ram_usage", "storage_usage", "performance_slowdown"]),
        ("Temperature", "Heat, cooling and fan behavior", ["cpu_temp", "gpu_temp", "fan_noise", "overheating", "dust_level", "thermal_paste_age", "last_maintenance", "loud_fans"]),
        ("Storage", "Drive type, health and boot signals", ["storage_type", "storage_health", "disk_errors", "slow_startup"]),
        ("Operating System", "Windows, drivers and application symptoms", ["blue_screen", "freezing", "crashes", "error_messages", "recent_driver_update", "recent_windows_update", "malware_symptoms", "black_screen", "screen_artifacts", "boot_failure"]),
        ("Network", "Internet and Wi-Fi connectivity", ["internet_problems", "wifi_problems"]),
        ("Power", "Shutdowns, restarts and power delivery", ["random_shutdowns", "system_restarts", "power_issues"]),
    ],
    "smartphone": [
        ("Device Information", "Capacity and current device state", ["storage_usage", "ram_usage"]),
        ("Battery", "Health, drain and heat", ["battery_health", "drain_rate", "temperature", "overheating"]),
        ("Charging", "Charging speed and connection", ["charge_minutes", "charging_failure"]),
        ("Performance", "Stability during everyday use", ["app_crashes", "unexpected_restarts"]),
        ("Display & Touch", "Screen and touch behavior", ["screen_issue", "touch_issue"]),
        ("Camera", "Camera availability and output", ["camera_issue"]),
        ("Network", "Wi-Fi and mobile data", ["network_issue"]),
    ],
    "wifi": [
        ("Connection", "Which devices and links are affected", ["all_devices_affected", "wired_slow"]),
        ("Speed", "Download and upload performance", ["download_speed", "upload_speed", "connected_devices"]),
        ("Latency", "Ping and jitter", ["ping", "high_latency"]),
        ("Wi-Fi Signal", "Strength and reach", ["signal_strength", "weak_signal"]),
        ("Router", "Router stability", ["router_restarts"]),
        ("DNS", "Name-resolution errors", ["dns_error"]),
        ("Stability", "Connection dropouts", ["disconnects"]),
    ],
    "gaming": [
        ("Console", "Platform-wide symptoms", ["all_games_affected", "updates_pending"]),
        ("Performance", "Frame rate and crashes", ["fps_drop", "crashes"]),
        ("Graphics", "Visual output issues", ["artifacts"]),
        ("Temperature", "Heat and fan activity", ["temperature", "fan_noise", "overheating"]),
        ("Storage", "Available game storage", ["storage_free"]),
        ("Controller", "Input behavior", ["controller_issue"]),
        ("Network", "Online play quality", ["ping", "disconnects"]),
    ],
    "battery": [
        ("Battery", "Health, age and rate of drain", ["battery_health", "drain_rate", "device_age", "background_drain"]),
        ("Charging", "Charging rate and charger output", ["charge_minutes", "charger_wattage", "charging_failure"]),
        ("Temperature", "Battery temperature while in use", ["temperature"]),
        ("Safety", "Physical and cable condition", ["swelling", "cable_damage"]),
    ],
    "car": [
        ("Vehicle Information", "Vehicle age and baseline", ["age_years"]),
        ("Starting", "Battery and cranking symptoms", ["starting_failure", "battery_voltage", "cranking_slow"]),
        ("Engine", "Idle, exhaust and leaks", ["rough_idle", "smoke", "fluid_leak"]),
        ("Temperature", "Engine heat symptoms", ["engine_temp", "overheating"]),
        ("Warning Lights", "Dashboard signals", ["warning_light", "check_engine"]),
        ("Brakes", "Noise or vibration while braking", ["brake_noise"]),
    ],
    "home_electronics": [
        ("Device Information", "Choose the affected device", ["device_type", "age_years"]),
        ("Power", "Starting and power stability", ["power_failure", "intermittent_power"]),
        ("Display", "Image and video behavior", ["display_issue", "cable_changed"]),
        ("Audio", "Sound output", ["sound_issue"]),
        ("Connectivity", "Network or device links", ["connection_issue"]),
        ("Software", "Error codes and heat", ["error_code", "overheating", "paper_jam"]),
    ],
    "electrical": [
        ("Supply", "Power availability and voltage", ["outage", "voltage", "multiple_devices"]),
        ("Stability", "Fluctuations and shutdowns", ["voltage_fluctuation", "device_shutdown"]),
        ("Circuit", "Breaker and backup behavior", ["breaker_trip", "ups_alarm"]),
        ("Equipment", "Adapters and cables", ["adapter_hot", "cable_damage"]),
        ("Safety", "Surges, smell or sparks", ["surge_recent", "burning_smell"]),
    ],
}

for category, sequence in SEQUENCES.items():
    SPECS[category]["sequences"] = [
        {"title": title, "description": description, "fields": fields}
        for title, description, fields in sequence
    ]

CATEGORIES = [{k:v for k,v in spec.items() if k not in ("signatures","actions", "labels")} for spec in SPECS.values()]
