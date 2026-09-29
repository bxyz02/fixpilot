"""
Diagnosis metadata: description, icon, severity, symptoms and recommended
actions for each problem category. Mirrors the RECOMMENDATIONS object in
the active frontend modules so the backend and displayed labels stay aligned.
"""

RECOMMENDATIONS = {
    "CPU overheating": {
        "icon": "🔥", "severity": "warn",
        "description": "Your CPU is running hotter than it should. This is usually caused by dust, aging thermal paste, or a failing cooler.",
        "symptoms": ["High CPU temperature", "Loud fans", "Random shutdowns", "Performance throttling"],
        "actions": ["Check CPU temperature in BIOS/HWMonitor", "Clean dust from the CPU cooler",
                     "Verify CPU fan is spinning", "Inspect and reapply thermal paste",
                     "Improve case airflow and cable management", "Reduce CPU-heavy workloads temporarily"],
    },
    "GPU overheating": {
        "icon": "🎮", "severity": "warn",
        "description": "Your graphics card is thermal-throttling. Common on older GPUs or systems with poor case airflow.",
        "symptoms": ["High GPU temperature", "Screen artifacts under load", "Fan noise spikes", "Frame drops"],
        "actions": ["Clean GPU fans and heatsink", "Adjust fan curve in GPU software",
                     "Check GPU thermal paste", "Improve case airflow", "Lower graphics settings temporarily"],
    },
    "RAM problem": {
        "icon": "🧠", "severity": "warn",
        "description": "Memory errors are likely. Faulty RAM often causes BSODs, freezes, and application crashes.",
        "symptoms": ["Blue screen of death", "Frequent crashes", "System freezing", "High RAM usage"],
        "actions": ["Run Windows Memory Diagnostic", "Reseat RAM modules", "Test RAM sticks one at a time",
                     "Check RAM timings and voltage in BIOS", "Update BIOS/UEFI"],
    },
    "SSD/HDD problem": {
        "icon": "💾", "severity": "warn",
        "description": "Your storage drive shows signs of degradation. Back up important data immediately.",
        "symptoms": ["Disk errors reported", "Slow startup", "File corruption", "High storage usage"],
        "actions": ["Check SMART status with CrystalDiskInfo", "Back up important files immediately",
                     "Run chkdsk /f /r", "Check available storage space", "Replace failing drive"],
    },
    "Power supply problem": {
        "icon": "⚡", "severity": "warn",
        "description": "Unstable power delivery. A failing PSU causes random shutdowns and boot failures.",
        "symptoms": ["Random shutdowns", "Power issues", "System restarts", "Boot failure"],
        "actions": ["Check power cable connections", "Test with a known-good PSU",
                     "Check PSU wattage vs system draw", "Inspect for burning smells or bulging caps",
                     "Replace PSU if symptoms persist"],
    },
    "Windows/software problem": {
        "icon": "🪟", "severity": "warn",
        "description": "Operating system or software corruption. Often follows a failed update or registry damage.",
        "symptoms": ["Error messages", "Application crashes", "Slow startup", "Performance slowdown"],
        "actions": ["Run sfc /scannow in admin CMD", "Run DISM /Online /Cleanup-Image /RestoreHealth",
                     "Check for pending Windows updates", "Uninstall recently added software",
                     "Consider System Restore"],
    },
    "Driver problem": {
        "icon": "🔧", "severity": "warn",
        "description": "Driver conflicts are destabilizing the system. Very common after a recent driver update.",
        "symptoms": ["Blue screen after update", "Device malfunctions", "Freezing", "Error messages"],
        "actions": ["Roll back the recent driver update", "Use DDU for clean GPU driver install",
                     "Update chipset drivers from manufacturer", "Check Device Manager for yellow warnings",
                     "Boot into Safe Mode to isolate"],
    },
    "Network adapter problem": {
        "icon": "📡", "severity": "warn",
        "description": "Your network hardware or driver is failing to maintain stable connectivity.",
        "symptoms": ["Internet problems", "Wi-Fi issues", "Frequent disconnects", "Slow speeds"],
        "actions": ["Update network adapter driver", "Reset network stack: netsh int ip reset",
                     "Forget and reconnect Wi-Fi", "Check router firmware", "Try a wired connection to isolate"],
    },
    "Motherboard problem": {
        "icon": "🔩", "severity": "warn",
        "description": "Possible motherboard-level issue. Multiple subsystems failing together often points here.",
        "symptoms": ["Multiple component failures", "Boot failure", "Power issues", "Random shutdowns"],
        "actions": ["Reset CMOS / BIOS to defaults", "Check for bulging capacitors", "Reseat all connectors",
                     "Test with minimal hardware", "Consider professional diagnosis"],
    },
    "Malware/security problem": {
        "icon": "🛡", "severity": "warn",
        "description": "Suspicious behavior consistent with malware or unwanted software.",
        "symptoms": ["Malware symptoms", "High CPU usage", "Error messages", "Performance slowdown"],
        "actions": ["Run a full scan with Windows Defender", "Scan with Malwarebytes",
                     "Check Task Manager for unknown processes", "Review startup programs",
                     "Consider a clean Windows reinstall"],
    },
    "Cooling problem": {
        "icon": "❄", "severity": "warn",
        "description": "General cooling deficiency — dust, aging paste, or insufficient airflow.",
        "symptoms": ["High dust level", "Old thermal paste", "Loud fans", "Elevated temperatures"],
        "actions": ["Deep-clean the entire system", "Replace thermal paste on CPU/GPU",
                     "Add or reposition case fans", "Check fan curves in BIOS", "Improve room ventilation"],
    },
    "Display/GPU problem": {
        "icon": "🖥", "severity": "warn",
        "description": "Visual output issues — may be the GPU, cable, or display itself.",
        "symptoms": ["Screen artifacts", "Black screen", "Display flickering", "No signal"],
        "actions": ["Test with another cable", "Try a different monitor", "Reseat GPU in PCIe slot",
                     "Update or reinstall GPU driver", "Check GPU power connectors"],
    },
    "Boot problem": {
        "icon": "🚀", "severity": "warn",
        "description": "System fails to boot or takes excessively long to start.",
        "symptoms": ["Boot failure", "Black screen at startup", "Slow startup", "Blue screen on boot"],
        "actions": ["Check BIOS boot order", "Disconnect non-essential peripherals", "Run Startup Repair",
                     "Boot into Safe Mode", "Check storage drive health"],
    },
    "Performance problem": {
        "icon": "📉", "severity": "warn",
        "description": "System is sluggish. Usually a combination of software bloat and resource pressure.",
        "symptoms": ["Performance slowdown", "High RAM usage", "High storage usage", "Application crashes"],
        "actions": ["Disable startup programs", "Free up disk space", "Check for malware",
                     "Upgrade RAM or switch to SSD", "Clean install of Windows if needed"],
    },
    "Unknown": {
        "icon": "❓", "severity": "ok",
        "description": "Insufficient or conflicting signals. The model cannot confidently classify this case.",
        "symptoms": ["No strong indicator found"],
        "actions": ["Provide more complete information", "Run built-in hardware diagnostics",
                     "Monitor temperatures and usage over time", "Check Windows Event Viewer for clues"],
    },
}
