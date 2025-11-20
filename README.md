
# **Delivery Scheduling Optimization (VRPTW)**

*A G-OPT Case Study*

This project demonstrates a **Vehicle Routing Problem with Time Windows (VRPTW)** solved using:

* 🕒 Customer delivery time windows
* 🚚 Multiple vehicles
* ⏳ Waiting time handling
* 📍 Realistic travel times
* ⚙️ Google OR-Tools routing engine

This project is part of the official **G-OPT** optimization portfolio, showcasing practical scheduling solutions for small companies in Finland and the Nordic region.

---

## 🔍 **Features**

* Multi-driver delivery scheduling
* Time window constraints (earliest & latest delivery)
* Realistic travel-time matrix generated from coordinates
* Automatic computation of arrival times
* Perfect for small logistics and delivery services
* Clear and interpretable console output
* Optional map visualization (PNG)

---

## 📁 **Project Files**

| File                             | Description                                         |
| -------------------------------- | --------------------------------------------------- |
| `vrptw.py`                       | Main VRPTW optimization solver                      |
| `delivery_vrptw.csv`             | Example dataset with time windows                   |
| `vrptw_plot.py`                  | Map visualization script (optional)                 |
| `delivery_vrptw.png`             | Visualization result (generated after running plot) |
| `gopt_case_study_scheduling.pdf` | Professional G-OPT case study (1 page)              |
| `README.md`                      | Project documentation                               |

---

## 🧠 **Optimization Model**

This project uses:

* OR-Tools Routing Model
* Haversine distance for realistic travel estimations
* Time dimension (`AddDimension`)
* Allowed waiting time for early arrivals
* Hard time-window constraints
* PATH_CHEAPEST_ARC + Guided Local Search

This setup mimics real conditions for small delivery businesses.

---

## ▶️ **How to Run**

Install required packages:

```bash
pip install ortools pandas numpy geopandas shapely contextily matplotlib
```

Run the delivery scheduling solver:

```bash
python vrptw.py
```

This prints:

* Route for each vehicle
* Arrival times at each location
* Satisfaction of time windows

(Optional) Generate map visualization:

```bash
python vrptw_plot.py
```

This produces:

* `delivery_vrptw.png` (map with route paths and arrows)

---

## 🧾 **Case Study**

A professional 1-page G-OPT case study is included:

* `gopt_case_study_scheduling.pdf`

Suitable for proposals, portfolios, client demonstrations, and business presentations.

---

## 🏢 **About G-OPT**

**G-OPT (Global Optimization)** provides intelligent and affordable optimization solutions for:

* Delivery route optimization
* Delivery scheduling
* Logistics analytics
* Technician & service routing

Helping Nordic small businesses reduce fuel cost, travel time, and operational complexity.
