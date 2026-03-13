# 🌍 Eco-Flow & System-Optimal Navigation App

A modern web application built with **Next.js (App Router)** and **Mapbox GL JS** that challenges the traditional "selfish" routing models (like Google Maps) by focusing on **System-Optimal Routing**. 

Instead of just finding the absolute fastest route for a single driver — which often creates bottlenecks and traffic jams elsewhere — our application calculates the best route for the *entire traffic ecosystem*. To incentivize drivers to choose these system-friendly routes, the app introduces an innovative **Driver Profiling and Gamification** system, tailoring the navigation experience to individual behaviors and needs.

![Project Preview](<img width="1008" height="562" alt="Image" src="https://github.com/user-attachments/assets/e51d88fb-724f-4c56-bfed-32bb4efc3db2" />) ## ✨ Key Features

* **🌍 System-Optimal vs. Selfish Routing:** Traditional navigation apps route everyone through the exact same "fastest" path, causing congestion. Our app distributes traffic intelligently to optimize the global city network, offering a "Personalized" route alongside the standard fastest one.
* **🎭 Driver Profiling & "Characters":** We understand that every driver has different needs. The app creates a customizable "Character" for each user based on their specific driving style:
    * **Dynamic:** For drivers who prefer to keep moving and avoid standing in traffic.
    * **Safe:** Prioritizing wider roads, fewer complex intersections, and calmer traffic (e.g., parents driving with children).
    * **Vibe/Chill:** For relaxed, scenic driving without the stress of rush hour.
* **🎮 Gamification & Karma Points:** Users are actively rewarded for choosing the system-optimal route. They earn "Karma Points" (eco-points) that instantly update in the UI via React Context API, creating a positive feedback loop.
* **🤖 Future-Ready AI Integration (Roadmap):** The customized user profiles lay the foundation for future Machine Learning models. The system will learn individual behaviors to automatically predict and suggest the perfect system-optimal route that naturally aligns with the user's specific "character."
* **🗺️ Interactive Maps & Multi-Routing:** Deep integration with Mapbox GL JS to simultaneously render and compare multiple routes on the fly, with dynamic styling based on the user's selected driving style.
* **⚛️ Custom Mapbox + React Portals:** Resolves React 18 Strict Mode and DOM-detachment issues by rendering custom UI markers securely inside Mapbox canvases using React Portals.
* **🔐 Secure Authentication:** Token-based authentication (JWT) handled via Next.js Server Actions and secure `HttpOnly` cookies, including PRG (Post-Redirect-Get) flow.
  
## 🛠️ Tech Stack

* **Framework:** [Next.js](https://nextjs.org/) (App Router, Server Actions)
* **UI Library:** React 18
* **Styling:** [Tailwind CSS](https://tailwindcss.com/), [shadcn/ui](https://ui.shadcn.com/)
* **Mapping:** [Mapbox GL JS](https://www.mapbox.com/)
* **State Management:** React Context API
* **Language:** TypeScript
* **Backend (API):** Integrates with a FastAPI backend.

## 🚀 Getting Started

### Prerequisites

Ensure you have **Node.js** (v18+) installed. You will also need API keys for Mapbox and your running FastAPI backend.

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/<YOUR_REPO_NAME>.git
   cd <YOUR_REPO_NAME>
