# Solar Panel API

This is a RESTful API for managing solar panel data, user authentication, and password reset functionality.

## Table of Contents

- [Features](#features)
  - [1. CanFrames Resource](#1-canframes-resource)
  - [2. Login Resource](#2-login-resource)
  - [3. Reset Password Resource](#3-reset-password-resource)
- [Technical Details](#technical-details)
- [Example Usage](#example-usage)
  - [Create a new CAN frame](#create-a-new-can-frame)
  - [Login user](#login-user)
- [Setup](#setup)
- [Notes](#notes)
- [License](#license)

## Features

### 1. CanFrames Resource

Manage solar panel CAN frames data.

- **GET /can_frames**  
  Retrieves all CAN frames records, ordered by date descending.

- **GET /can_frames/{id}**  
  Retrieves a single CAN frame record by its ID.

- **POST /can_frames**  
  Creates a new CAN frame record.  
  **Required JSON fields:**  
  `east`, `west`, `north`, `average`, `v_panel`, `v_battery`, `c_panel`, `c_battery`, `charge_state`, `light_on`, `light_lvl`, `curr_elev`, `curr_azim`, `angle_azim`, `angle_elev`, `corr_mode`, `corr_interval`, `corr_threshold`

- **PUT /can_frames/{id}**  
  Updates an existing CAN frame record by ID. Same fields as POST.

- **DELETE /can_frames/{id}**  
  Deletes a CAN frame record by ID.

---

### 2. Login Resource

Basic user authentication.

- **POST /login**  
  Authenticates a user with email and password.  
  **Required JSON fields:**  
  `email`, `password`

---

### 3. Reset Password Resource

Manage password reset tokens.

- **POST /reset_password**  
  (Implementation details assumed) Create a reset token for the given email.

- **PUT /reset_password**  
  (Implementation details assumed) Validate and use a reset token to update the password.

---

## Technical Details

- Uses MySQL for data storage.
- Passwords are securely hashed using PHP's `password_hash` and verified with `password_verify`.
- CORS enabled for all origins.
- All responses are in JSON format.
- Proper HTTP status codes are used for success and errors.

---

## Example Usage

### Create a new CAN frame

```bash
curl -X POST https://yourdomain.com/api/can_frames \
-H "Content-Type: application/json" \
-d '{
  "east": 10,
  "west": 12,
  "north": 11,
  "average": 11,
  "v_panel": 120,
  "v_battery": 115,
  "c_panel": 5,
  "c_battery": 3,
  "charge_state": 1,
  "light_on": 0,
  "light_lvl": 50,
  "curr_elev": 30,
  "curr_azim": 60,
  "angle_azim": 15,
  "angle_elev": 10,
  "corr_mode": 2,
  "corr_interval": 5,
  "corr_threshold": 3
}'


http://localhost/api/index.php?path=can_frames