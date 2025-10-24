from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from admin.model.users_model import get_users
from admin.model.categories_model import get_categories, get_category_by_id, add_category, delete_category
from admin.model.products_model import get_products, add_product, delete_product
from . import admin_route
from .image_uploader import upload_image_to_cloudinary

@admin_route.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title="Trang quản trị HomeMadeCoffee")

@admin_route.route("/users")
def users():
    users = get_users()
    total_user = len(users)
    return render_template("users.html", 
                           title="Quản lý người dùng", 
                           users=users, 
                           total_user=total_user)

@admin_route.route("/products/<int:category_id>")
def products(category_id):
    products_list =  get_products(category_id)

    category_name = get_category_by_id(category_id)

    if not category_id or category_id == 0:
        flash("Danh mục không hợp lệ", "error")
        return redirect(url_for("admin_route.category"))
        
    total_product = len(products_list)
    return render_template("products.html", 
                            title="Quản lý sản phẩm",
                            category_name=category_name['category_name'],
                            category_id=category_id,
                            products=products_list,
                            total_product=total_product)

@admin_route.route("/add_product", methods=["GET", "POST"])
def add_product_route():
    if request.method == "POST":
        # Lấy id danh mục từ form thêm sản phẩm
        category_id = request.form.get("product-category", "").strip()

        if 'product-image' not in request.files:
            flash("Lỗi Form: Thiếu trường 'product-image'. Liên hệ dev.", "error")
            return redirect(url_for("admin_route.products", category_id=category_id))

        file = request.files.get('product-image')

        if not file or file.filename == '':
            flash("Vui lòng chọn một file ảnh cho sản phẩm.", "error")
            return redirect(url_for("admin_route.products", category_id=category_id))

        image_url = None

        try:
            print(f"Uploading file '{file.filename}' to Cloudinary...")
            image_url, upload_message = upload_image_to_cloudinary(file)

            if not image_url:
                # Nếu upload thất bại, báo lỗi và dừng lại
                flash(f"Lỗi tải ảnh lên: {upload_message}", "error")
                return redirect(url_for("admin_route.products", category_id=category_id))
            
            print(f"File uploaded successfully. URL: {image_url}")

            product_name = request.form.get("product-name", "").strip()
            description = request.form.get("description", "").strip()
            price = request.form.get("product-price", "").strip()

            # Kiểm tra thông tin có được nhập trong form hay không
            if not category_id or category_id == 0:
                flash("Vui lòng chọn danh mục", "error")
                return redirect(url_for("admin_route.products", category_id=category_id))
            
            if not product_name:
                flash("Vui lòng nhập tên sản phẩm", "error")
                return redirect(url_for("admin_route.products", category_id=category_id))
            
            if not description:
                flash("Vui lòng nhập mô tả sản phẩm", "error")
                return redirect(url_for("admin_route.products", category_id=category_id))
            
            if not price:
                flash("Vui lòng nhập giá sản phẩm", "error")
                return redirect(url_for("admin_route.products", category_id=category_id))
            
            if not image_url:
                flash("Vui lòng nhập URL hình ảnh sản phẩm", "error")
                return redirect(url_for("admin_route.products", category_id=category_id))
            
            success, message = add_product(product_name, description, float(price), image_url, int(category_id))

            flash(message, "success" if success else "error")
        
        except ValueError:
            flash("Giá sản phẩm phải là một con số (ví dụ: 50000).", "error")
        except Exception as e:
            print(f"Error uploading product: {str(e)}", file=sys.stderr)
            flash(f"Lỗi khi tải ảnh lên: {str(e)}", "error")
        
        return redirect(url_for("admin_route.products", category_id=category_id))

@admin_route.route("/delete_product/<int:product_id>/<int:category_id>", methods=["POST"])
def delete_product_route(product_id, category_id):
    """Xoá sản phẩm"""
    success, message = delete_product(product_id)
    flash(message, "success" if success else "error")

    return redirect(url_for("admin_route.products", category_id=category_id))

@admin_route.route("/categories")
def category():
    categories = get_categories()
    total_category = len(categories)
    return render_template("categories.html",
                            title="Quản lý danh mục", 
                            categories=categories, 
                            total_category=total_category)

@admin_route.route("/add_category", methods=["GET", "POST"])
def add_category_route():
    if request.method == "POST":
        # Lấy dữ liệu từ form thêm danh mục
        category_name = request.form.get("category-name", "").strip()
        description = request.form.get("description", "").strip()

        # Kiểm tra thông tin có được nhập trong form hay không
        if not category_name:
            flash("Vui lòng nhập tên danh mục", "error")
            return redirect(url_for("admin_route.category"))
        
        if not description:
            flash("Vui lòng nhập mô tả của danh mục", "error")
            return redirect(url_for("admin_route.category"))
        
        success, message = add_category(category_name, description)

        flash(message, "success" if success else "error")

        return redirect(url_for("admin_route.category"))

@admin_route.route("/delete_category/<int:category_id>", methods=["POST"])
def delete_category_route(category_id):
    """Xoá danh mục"""
    success, message = delete_category(category_id)
    flash(message, "success" if success else "error")

    return redirect(url_for("admin_route.category"))

@admin_route.route("/orders")
def orders():
    return render_template("orders.html", title="Quản lý đơn hàng")




