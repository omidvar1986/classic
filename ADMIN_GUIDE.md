# 🎯 Admin Guide: Managing Accessories & Pricing

## 📋 **Quick Access**
- **Admin Panel:** `http://127.0.0.1:8000/admin/`
- **Username:** (your admin username)
- **Password:** (your admin password)

---

## 🛠️ **Managing Accessories**

### **Adding New Accessories**

1. **Go to Admin Panel** → **Print_service** → **Accessories**
2. **Click "Add Accessory"**
3. **Fill in the details:**
   - **Name:** e.g., "Premium Binding"
   - **Description:** Detailed description of the accessory
   - **Base Price:** Price in Tomans (e.g., 25000)
   - **Category:** Choose from:
     - `binding` - Binding Options (wiring, staples, etc.)
     - `finishing` - Finishing Options (lamination, coating, etc.)
     - `packaging` - Packaging Options (envelopes, folders, etc.)
     - `paper` - Paper Options (special paper types)
   - **Service Type:** Choose from:
     - `print` - Only for print service
     - `typing` - Only for typing service
     - `both` - For both services
   - **Is Active:** Check to enable the accessory
   - **Icon:** FontAwesome icon class (e.g., `fas fa-star`)
   - **Sort Order:** Display order (lower numbers appear first)

### **Editing Existing Accessories**

1. **Go to Admin Panel** → **Print_service** → **Accessories**
2. **Click on any accessory name** to edit
3. **Modify any field** and click "Save"

### **Managing Accessory Prices**

- **Change Base Price:** Edit the "Base Price" field
- **Bulk Price Update:** Use the list view to quickly see all prices
- **Enable/Disable:** Use "Is Active" checkbox to show/hide accessories

---

## 💰 **Managing Service Pricing**

### **Print Service Pricing**

1. **Go to Admin Panel** → **Print_service** → **Print Price Settings**
2. **Configure:**
   - **Base Price Per Page:** Default price per page (e.g., 50000 تومان)
   - **Color Price Multiplier:** How much more expensive color printing is (e.g., 1.5 = 50% more)
   - **Double-Sided Discount:** Discount for double-sided printing (e.g., 0.8 = 20% discount)

### **Typing Service Pricing**

1. **Go to Admin Panel** → **Typing_service** → **Typing Price Settings**
2. **Set Price Per Page:** Base price for typing service (e.g., 10000 تومان)

---

## 📦 **Managing Package Deals**

### **Creating Package Deals**

1. **Go to Admin Panel** → **Print_service** → **Package Deals**
2. **Click "Add Package Deal"**
3. **Fill in:**
   - **Name:** e.g., "Professional Package"
   - **Description:** What's included in the package
   - **Discount Price:** Final package price
   - **Original Price:** Sum of individual accessory prices
   - **Service Type:** Print, Typing, or Both
   - **Accessories:** Select multiple accessories to include
   - **Is Active:** Enable/disable the package

### **Example Package Deal:**
- **Name:** "Complete Professional Package"
- **Accessories:** Wire Binding + Lamination + Folder
- **Original Price:** 45000 تومان
- **Discount Price:** 40000 تومان
- **Savings:** 5000 تومان

---

## 📊 **Viewing Order Details with Accessories**

### **Print Orders**
1. **Go to Admin Panel** → **Print_service** → **Print Orders**
2. **Click on any order** to view details
3. **Scroll down** to see "Selected Accessories" section
4. **View:**
   - Each selected accessory
   - Quantity and price
   - Total accessories cost
   - Final order total

### **Typing Orders**
1. **Go to Admin Panel** → **Typing_service** → **Typing Orders**
2. **Click on any order** to view details
3. **See accessories** in the inline section
4. **View total pricing** including accessories

---

## 🔧 **Quick Admin Actions**

### **Bulk Operations**
- **Select multiple accessories** in the list view
- **Use "Actions" dropdown** for bulk operations
- **Quick price updates** by editing multiple items

### **Search & Filter**
- **Search accessories** by name or description
- **Filter by category** (Binding, Finishing, etc.)
- **Filter by service type** (Print, Typing, Both)
- **Filter by active status**

### **Export Data**
- **Use Django admin's export features** to download order data
- **View pricing reports** in the admin interface

---

## 💡 **Pro Tips**

### **Pricing Strategy**
1. **Start with competitive base prices**
2. **Use accessories for premium services**
3. **Create package deals for popular combinations**
4. **Regularly review and adjust prices**

### **Accessory Management**
1. **Use descriptive names** that customers understand
2. **Add helpful descriptions** explaining the value
3. **Use appropriate icons** for visual appeal
4. **Group related accessories** in the same category

### **Customer Experience**
1. **Keep popular accessories active**
2. **Disable seasonal or discontinued items**
3. **Update prices regularly** based on costs
4. **Monitor which accessories are most popular**

---

## 🚨 **Important Notes**

- **Only one pricing settings object** can exist per service
- **Accessories are shared** between print and typing services
- **Price changes affect new orders only** (existing orders keep original prices)
- **Always test pricing changes** before making them live
- **Backup your data** before making major changes

---

## 📞 **Need Help?**

If you encounter any issues:
1. **Check the Django admin logs**
2. **Verify all required fields are filled**
3. **Ensure prices are positive numbers**
4. **Contact your system administrator**

---

**🎉 You're all set to manage accessories and pricing like a pro!** 