# LendShield Deployment Guide

This guide will help you deploy the **LendShield** application to the web. We will use **Render** for the Python Backend and **Vercel** for the React Frontend.

## Prerequisites
- A GitHub account with this repository pushed to it.
- Accounts on [Render](https://render.com) and [Vercel](https://vercel.com).

---

## 1. Backend Deployment (Render)

1.  Log in to your **Render** dashboard.
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub repository.
4.  Render should automatically detect the `render.yaml` file I created in the root of your project.
5.  Click **Apply** or **Create Service**.
    *   *Note: If Blueprint doesn't work for any reason, create a "Web Service" with:*
        *   *Root Directory:* `.`
        *   *Build Command:* `pip install -r backend/requirements.txt`
        *   *Start Command:* `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6.  Wait for the deployment to finish.
7.  **Copy the URL** of your new backend service (e.g., `https://lendshield-backend.onrender.com`). You will need this for the frontend.

---

## 2. Frontend Deployment (Vercel)

1.  Log in to your **Vercel** dashboard.
2.  Click **Add New...** -> **Project**.
3.  Import your **LendShield** Git repository.
4.  **Configure Project**:
    *   **Root Directory**: Click `Edit` and select `frontend`.
    *   **Framework Preset**: Keep as `Vite`.
    *   **Environment Variables**:
        *   Key: `VITE_API_URL`
        *   Value: *Paste your Render Backend URL here* (no trailing slash, e.g., `https://lendshield-backend.onrender.com`)
5.  Click **Deploy**.

---

## 3. Verification

Once Vercel finishes deploying:
1.  Open your Vercel App URL.
2.  Check the "Dashboard" and ensure data is loading (it might take a minute for the Render backend to wake up if on the free tier).
3.  Try "Simulate New Application" to verify the AI model is responding.
