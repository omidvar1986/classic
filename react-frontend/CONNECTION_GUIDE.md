# 🔗 React to Django Connection Guide

## 📋 **Complete Setup Instructions**

### **Step 1: Start Django Backend**

Open **Terminal 1** and run:
```bash
cd /Users/miladomidvar/Desktop/Djangoproject/calssic_sys
source venv/bin/activate
python3 manage.py runserver 8000
```

**Expected Output:**
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
August 05, 2025 - 14:00:00
Django version 4.2.23, using settings 'smart_office.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### **Step 2: Start React Frontend**

Open **Terminal 2** and run:
```bash
cd /Users/miladomidvar/Desktop/Djangoproject/calssic_sys/react-frontend
npm run dev
```

**Expected Output:**
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully in 2.3s (18 modules)
```

### **Step 3: Test the Connection**

1. **Open your browser** and go to: `http://localhost:3000`
2. **You should see** the React home page with glow cards
3. **Click "ورود به سیستم"** to test login
4. **Use your existing Django user credentials**

## 🔧 **What We've Configured**

### **Django Backend Changes:**

1. **CORS Settings** - Added to `smart_office/settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
   ]
   CORS_ALLOW_CREDENTIALS = True
   ```

2. **API Endpoints** - Added to `accounts/views.py`:
   - `/accounts/api/login/` - Login API
   - `/accounts/api/register/` - Registration API
   - `/accounts/api/logout/` - Logout API
   - `/accounts/api/profile/` - Get user profile

3. **URL Configuration** - Updated `accounts/urls.py` with API routes

### **React Frontend Changes:**

1. **API Service** - Updated `src/lib/api.ts` to use Django endpoints
2. **Authentication Context** - Updated to handle Django API responses
3. **Login/Register Pages** - Updated error handling
4. **Environment Variables** - Set API URL to Django server

## 🧪 **Testing Steps**

### **Test 1: Home Page**
- Go to `http://localhost:3000`
- Should see beautiful home page with glow cards
- Should see "ورود به سیستم" and "ثبت نام" buttons

### **Test 2: Login**
- Click "ورود به سیستم"
- Enter your existing Django user credentials
- Should redirect to dashboard on success

### **Test 3: Registration**
- Click "ثبت نام" on home page
- Fill out the form with new user details
- Should create new user and redirect to dashboard

### **Test 4: Dashboard**
- After login, should see dashboard with:
  - User statistics
  - Glow cards for each service
  - User profile information

## 🐛 **Troubleshooting**

### **If React shows "Cannot connect to API":**
1. Make sure Django is running on port 8000
2. Check browser console for CORS errors
3. Verify `.env.local` has correct API URL

### **If Login fails:**
1. Check Django server logs for errors
2. Verify user exists in Django admin
3. Check browser network tab for API calls

### **If CORS errors occur:**
1. Restart Django server after CORS changes
2. Clear browser cache
3. Check CORS settings in Django

## 📱 **Access Points**

- **React Frontend**: `http://localhost:3000`
- **Django Backend**: `http://127.0.0.1:8000`
- **Django Admin**: `http://127.0.0.1:8000/admin/`

## 🔄 **Development Workflow**

1. **Make changes to React** → Auto-reloads
2. **Make changes to Django** → Auto-reloads
3. **Both servers run simultaneously**
4. **React calls Django APIs** for data

## 🎯 **Next Steps**

After successful connection:
1. Test all authentication flows
2. Add more API endpoints for orders
3. Implement real-time features
4. Add error handling and loading states

---

**✅ If you see the React home page with glow cards, the connection is working!** 