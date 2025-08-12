from flask import Flask, render_template, request, jsonify, session
import sqlite3

#laptop venv
#source myenv/bin/activate

#desktop venv
#myenv\Scripts\activate.bat

app = Flask(__name__)

# pull from db
# basic part data
def get_parts(category):
    conn = sqlite3.connect("spare_parts.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {category}")

    parts = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.close()

    return {"columns": column_names, "rows": parts}

# details from parts, specs price etc
def get_part_details(part_name):
    conn = sqlite3.connect("spare_parts.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM parts WHERE name = ?", (part_name,))

    part = cursor.fetchone()
    conn.close()
    
    if part:
        return {
            "name": part[0],
            "price": part[1],
            
            "core_count": part[2] if part[2] else "N/A",
            "core_clock": part[3] if part[3] else "N/A",
            "boost_clock": part[4] if part[4] else "N/A"
                                                    #print N/a to avoid nulls
        }
    else:
        return {}

# routing
# homepage
@app.route("/")
def main():
    return render_template("main.html")

# pc builder
@app.route("/index")
def index():
    categories = ["cpu", "cpu_cooler", "motherboard", "memory", "storage", "video_card", "pc_case", "power_supply", "operating_system"]
    parts_data = {}

    for category in categories:
        key = category
        parts_data[key] = get_parts(key)
    selected_parts = session.get("selected_parts", {})


    return render_template("index.html", parts_data=parts_data, selected_parts=selected_parts)

#incomplete pre-build pages, students, pros, content creators
@app.route("/students")
def students():
    return render_template("students.html")

@app.route("/pros")
def pros():
    return render_template("pros.html")

@app.route("/cc")
def cc():
    return render_template("cc.html")

#save build for checkout page
@app.route("/save_build", methods=["POST"])
def save_build():
    data = request.get_json()

    # required parts for a completed build
    required_parts = [
        "cpu", "cpu_price", "cpu_core_count", "cpu_core_clock", "cpu_boost_clock",
        "cpu_cooler", "cpu_cooler_price", "motherboard", "motherboard_price", 
        "memory", "memory_price", "storage", "storage_price", "video_card", 
        "video_card_price", "pc_case", "pc_case_price", "power_supply", 
        "power_supply_price", "operating_system", "operating_system_price", "total_price"
    ]
    
    # make sure build has all needed parts
    for part in required_parts:
        if part not in data or not isinstance(data[part], (str, float, int)):
            #tell user if a part is missing and whiuch one
            return jsonify({"success": False, "error": f"Missing {part}"}), 400

    # save completed build in user_builds table
    try:
        conn = sqlite3.connect("spare_parts.db")
        cursor = conn.cursor()
        print(data)
        #core count , clock, boost clock, are unused atm
        # add more specs to other data stretch.. fix table with new structure
        # ignore those specs for now 
        cursor.execute("""
            INSERT INTO user_builds (
                cpu, cpu_price, cpu_core_count, cpu_core_clock, cpu_boost_clock,
                cpu_cooler, cpu_cooler_price, motherboard, motherboard_price,
                memory, memory_price, storage, storage_price, video_card,
                video_card_price, pc_case, pc_case_price, power_supply,
                power_supply_price, operating_system, operating_system_price, total_price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["cpu"], data["cpu_price"], data["cpu_core_count"], data["cpu_core_clock"], 
            data["cpu_boost_clock"], data["cpu_cooler"], data["cpu_cooler_price"], 
            data["motherboard"], data["motherboard_price"], data["memory"], data["memory_price"], 
            data["storage"], data["storage_price"], data["video_card"], data["video_card_price"], 
            data["pc_case"], data["pc_case_price"], data["power_supply"], 
            data["power_supply_price"], data["operating_system"], data["operating_system_price"], data["total_price"]
        ))

        #debug
        #cursor.execute("PRAGMA table_info(user_builds);")
        #columns = cursor.fetchall()
        #print(columns)
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        # debug
        #print(f"Error saving build: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


#checkout route, send saved build to checkout page
@app.route("/checkout")
def checkout():
    conn = sqlite3.connect("spare_parts.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_builds ORDER BY id DESC LIMIT 1")
    build = cursor.fetchone()
    conn.close()

    #handle no build found
    if not build:
        return render_template("error.html", message="No build found. Please complete a build first.")

    #completed build dict
    build_dict = {
        "cpu": build[1],
        "cpu_price": build[2],
        "cpu_core_count": build[3],
        "cpu_core_clock": build[4],
        "cpu_boost_clock": build[5],
        "cpu_cooler": build[6],
        "cpu_cooler_price": build[7],
        "motherboard": build[8],
        "motherboard_price": build[9],
        "memory": build[10],
        "memory_price": build[11],
        "storage": build[12],
        "storage_price": build[13],
        "video_card": build[14],
        "video_card_price": build[15],
        "pc_case": build[16],
        "pc_case_price": build[17],
        "power_supply": build[18],
        "power_supply_price": build[19],
        "operating_system": build[20],
        "operating_system_price": build[21],
        "total_price": build[22],
    }
    #debug, proof of working buiild
    #print(f"Build Data: {build_dict}")
    return render_template("checkout.html", build=build_dict)


# db compatibility
@app.route("/get_compatible_parts", methods=["POST"])
def get_compatible_parts():
    conn = sqlite3.connect("spare_parts.db")
    cursor = conn.cursor()
    selected_parts = request.get_json()
    compatibility = {}

    # cpu motherboard compatibility
    if "cpu" in selected_parts:
        cpu_name = selected_parts["cpu"]
        cursor.execute("""
            SELECT motherboard_name FROM cpu_motherboard_compatibility
            WHERE LOWER(cpu_name) = LOWER(?)
        """, (cpu_name,))
        rows = cursor.fetchall()
        compatibility["motherboard"] = [row[0] for row in rows]


    # bi-directional compat, motherboard and cpu
    if "motherboard" in selected_parts:
        mobo_name = selected_parts["motherboard"]
        cursor.execute("""
            SELECT cpu_name FROM cpu_motherboard_compatibility
            WHERE LOWER(motherboard_name) = LOWER(?)
        """, (mobo_name,))

        compatibility["cpu"] = [row[0] for row in cursor.fetchall()]


    #motherboard mem compatibility
    if "motherboard" in selected_parts:
        mobo_name = selected_parts["motherboard"]
        cursor.execute("""
            SELECT memory_type, max_speed FROM motherboard_memory_compatibility
            WHERE LOWER(motherboard_name) = LOWER(?)
        """, (mobo_name,))
        specs = cursor.fetchone()

        if specs:
            memory_type, max_speed = specs
            cursor.execute("""
            SELECT name FROM memory
            WHERE type = ? AND speed <= ?
        """, (memory_type, max_speed))
            memory_compatible = [row[0] for row in cursor.fetchall()]
            compatibility["memory"] = memory_compatible

    # bi-directional compat, memory and motherboard
    if "memory" in selected_parts:
        mem_name = selected_parts["memory"]
        cursor.execute("""
            SELECT type, speed FROM memory
            WHERE LOWER(name) = LOWER(?)
        """, (mem_name,))
        specs = cursor.fetchone()

        if specs:
            mem_type, mem_speed = specs
            cursor.execute("""
                SELECT motherboard_name FROM motherboard_memory_compatibility
                WHERE memory_type = ? AND max_speed >= ?
        """, (mem_type, mem_speed))
            mobo_compatible = [row[0] for row in cursor.fetchall()]
            compatibility["motherboard"] = mobo_compatible

    # gpu case compat
    if "video_card" in selected_parts:
        cursor.execute("""
            SELECT case_name FROM gpu_case_compatibility
            WHERE gpu_name = ?
        """, (selected_parts["video_card"],))

        compatibility["pc_case"] = [row[0] for row in cursor.fetchall()]

    # gpu case bi-directional compat
    if "pc_case" in selected_parts:
        case_name = selected_parts["pc_case"]
        cursor.execute("""
            SELECT gpu_name FROM gpu_case_compatibility
            WHERE case_name = ?
        """, (case_name,))
        compatibility["video_card"] = [row[0] for row in cursor.fetchall()]

    # gpu power supply compat
    if "video_card" in selected_parts:
        gpu_name = selected_parts["video_card"]
        cursor.execute("""
            SELECT psu_name FROM gpu_psu_compatibility
            WHERE gpu_name = ?
        """, (gpu_name,))
        psu_compatible = [row[0] for row in cursor.fetchall()]
        compatibility["power_supply"] = psu_compatible

    # gpu power supply bi-directional compat
    if "power_supply" in selected_parts:
        psu_name = selected_parts["power_supply"]
        cursor.execute("SELECT wattage FROM power_supply WHERE name = ?", (psu_name,))
        psu = cursor.fetchone()
        if psu:
            psu_wattage = psu[0]
            cursor.execute("""
                SELECT gpu_name FROM gpu_psu_compatibility
                WHERE min_wattage_required <= ?
            """, (psu_wattage,))

            gpu_compatible = [row[0] for row in cursor.fetchall()]
            # dont overwrite existing compatibnility
            compatibility.setdefault("video_card", [])
            compatibility["video_card"] = list(set(compatibility["video_card"] + gpu_compatible)) # weird b/c psu and case noth have to be compat with gpu

    conn.close()
    return jsonify(compatibility)

#main
if __name__ == "__main__":
    app.run(debug=True)
