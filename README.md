# 🌍 EcoFlow – System-Optimal Navigation

A next-generation navigation platform that optimizes **city-wide traffic flow**, not just individual routes.

Unlike traditional navigation apps that route every driver through the same "fastest" path, **EcoFlow distributes traffic intelligently across the network**, reducing congestion and improving the overall traffic ecosystem.

Built with **Next.js, Mapbox GL JS, and FastAPI**.

---

## ✨ Overview

Most navigation apps (Google Maps, Waze) optimize for **User Equilibrium** — each driver selects the individually fastest route.

While optimal for a single driver, this often leads to:

- 🚧 Road overloading  
- 🚗 Traffic bottlenecks  
- 🌆 City-wide congestion  

**EcoFlow introduces System-Optimal Routing**, where traffic is distributed across multiple routes to minimize the **total travel time of the entire traffic network**.

To encourage drivers to adopt system-optimal routes, the application introduces **driver profiling and gamification**.

---

## 📸 Preview

![Project Preview](https://github.com/user-attachments/assets/e51d88fb-724f-4c56-bfed-32bb4efc3db)

---

# 🧩 Core Features

## 🌍 System-Optimal Routing

The application compares two navigation strategies:

| Strategy | Description |
|--------|-------------|
| **Selfish Routing** | Traditional fastest route for the individual driver |
| **System-Optimal Routing** | Traffic distributed to reduce global congestion |

Users can compare both routes directly on the map.

---

## 🎭 Driver Profiling

Drivers can select a navigation **character profile** based on their preferences.

### Dynamic
- prefers constant movement  
- avoids stop-and-go traffic  

### Safe
- prioritizes wider roads  
- fewer complex intersections  
- calmer traffic environments  

### Vibe / Chill
- relaxed driving  
- scenic routes  
- minimal rush-hour stress  

These profiles influence how routes are calculated and presented.

---

## 🎮 Gamification – Karma Points

Drivers who choose system-optimal routes receive **Karma Points**.

This creates a positive feedback loop:

- drivers help the overall traffic system
- they receive rewards in return

Points update instantly in the UI using **React Context state management**.

---

## 🗺️ Interactive Multi-Routing

Using **Mapbox GL JS**, the app renders:

- multiple route options
- dynamic styling based on driver profile
- interactive map layers

Users can visually compare route trade-offs.

---

## ⚛️ React + Mapbox Portal Integration

Custom map markers are rendered using **React Portals**, avoiding common issues with:

- React 18 Strict Mode
- DOM detachment in Mapbox canvases

This ensures stable UI rendering inside Mapbox layers.

---

## 🔐 Secure Authentication

Authentication is handled using:

- **JWT tokens**
- **Next.js Server Actions**
- **HttpOnly cookies**

The system follows the **Post-Redirect-Get (PRG) pattern** to prevent duplicate form submissions.

---

# 🏗️ Architecture

The project follows a **modern full-stack architecture**.

### Frontend

- Next.js (App Router)
- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui
- Mapbox GL JS

### Backend

- FastAPI
- Traffic routing algorithms
- Route scoring and system-optimal logic

### Communication

- REST API
- JWT authentication
- secure cookies

---

# 🧠 Future AI Integration

Driver profiles are designed to support future **machine learning models**.

Potential future features:

- driver behavior prediction
- AI-generated system-optimal routes
- adaptive route suggestions
- traffic pattern learning

---

# 🛠️ Tech Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Mapbox GL JS

## Backend

- FastAPI
- Python

---

# 🚀 Getting Started

## Prerequisites

Make sure you have installed:

- **Node.js 18+**
- **npm / yarn**
- **running FastAPI backend**
- **Mapbox API key**

---

## 🧭 Roadmap

### ✅ Completed

- [x] Multi-route visualization
- [x] Driver profiling system
- [x] Gamification (Karma Points)

---

### 🚧 In Progress

- [ ] Integration with real-time traffic services to detect road congestion
- [ ] Advanced routing algorithm for calculating multiple alternative paths
- [ ] Route selection based on driver profile (Dynamic / Safe / Chill)

---

### 🔮 Planned

- [ ] Partnership integrations (e.g. parking providers)
- [ ] Converting Karma Points into real-world rewards  
  - free parking
  - parking discounts
  - eco-driving incentives
- [ ] Smart route recommendations based on user driving behavior

---

### 🧠 AI & Data (Future Research)

- [ ] AI model for traffic prediction
- [ ] Driver behavior analysis using anonymized user data
- [ ] Personalized route generation using ML
- [ ] Traffic pattern prediction for city-wide optimization


## Installation

Clone the repository:

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git
cd <YOUR_REPO_NAME>
