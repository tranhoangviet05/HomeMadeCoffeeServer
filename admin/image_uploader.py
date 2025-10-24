import cloudinary
import cloudinary.uploader
import os
import sys

def configure_cloudinary():
    """
    Cấu hình Cloudinary từ Biến Môi Trường (Environment Variables).
    Đây là cách làm an toàn để không lộ 'bí mật' trong code.
    """
    try:
        cloudinary.config(
            cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key = os.environ.get('CLOUDINARY_API_KEY'),
            api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
            secure = True
        )
        print("Cloudinary configured successfully.")
    except Exception as e:
        print(f"FATAL: Could not configure Cloudinary. {e}", file=sys.stderr)
        
def upload_image_to_cloudinary(file_to_upload, public_id=None):
    """
    Tải file (dưới dạng stream) lên Cloudinary và trả về URL.
    """
    # Đảm bảo Cloudinary đã được cấu hình
    if not cloudinary.config().api_key:
        configure_cloudinary()
        
        # Nếu cấu hình vẫn thất bại (thiếu biến môi trường)
        if not cloudinary.config().api_key:
            return None, "Cloudinary is not configured."

    try:
        # Tải file lên
        upload_result = cloudinary.uploader.upload(
            file_to_upload,
            public_id=public_id, # Tên file (nếu có)
            overwrite=True,
            folder="products"    # Sắp xếp vào thư mục 'products' trên Cloudinary
        )
        
        # Lấy URL an toàn (https)
        secure_url = upload_result.get('secure_url')
        if secure_url:
            return secure_url, "Upload successful."
        else:
            return None, "Upload failed, no URL returned."

    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}", file=sys.stderr)
        return None, str(e)
