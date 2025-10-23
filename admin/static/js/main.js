/*
 * File: main.js
 * Chức năng: Xử lý bật/tắt modal cho nhiều trang
 */

document.addEventListener('DOMContentLoaded', function() {

    // --- Hàm chung để xử lý một modal ---
    // 'modalId' là ID của modal (ví dụ: 'add-category-modal')
    // 'openBtnId' là ID của nút mở modal (ví dụ: 'btn-add-category')
    function setupModal(modalId, openBtnId) {
        const modal = document.getElementById(modalId);
        const btnOpen = document.getElementById(openBtnId);

        // Nếu modal hoặc nút mở không tồn tại trên trang này, thì bỏ qua
        // (Điều này giúp code chạy an toàn trên tất cả các trang)
        if (!modal || !btnOpen) {
            return;
        }

        // Lấy TẤT CẢ các nút đóng bên trong modal cụ thể này
        const btnCloseList = modal.querySelectorAll('.btn-close-modal');

        // 1. Xử lý khi nhấn nút "Thêm"
        btnOpen.addEventListener('click', function() {
            modal.classList.add('modal-show');
        });

        // 2. Xử lý khi nhấn nút "Hủy" hoặc dấu "X"
        btnCloseList.forEach(function(btn) {
            btn.addEventListener('click', function() {
                modal.classList.remove('modal-show');
            });
        });

        // 3. Xử lý khi nhấn ra ngoài vùng form (lớp nền mờ)
        modal.addEventListener('click', function(event) {
            // Nếu nơi được click chính là lớp nền mờ (chứ không phải form)
            if (event.target === modal) {
                modal.classList.remove('modal-show');
            }
        });
    }

    // --- Áp dụng hàm cho từng cặp modal/nút ---
    
    // 1. Kích hoạt modal cho trang Danh mục
    setupModal('add-category-modal', 'btn-add-category');
    
    // 2. Kích hoạt modal cho trang Sản phẩm (MỚI)
    setupModal('add-product-modal', 'btn-add-product');

});

// Xử lý nút đóng cho thông báo flash
document.addEventListener('DOMContentLoaded', function() {
    
    // ... (Code modal của bạn giữ nguyên ở trên) ...

    // --- Xử lý đóng Flash Message ---
    const allFlashCloseButtons = document.querySelectorAll('.flash-close');
    
    allFlashCloseButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // "this.parentElement" chính là div.flash
            this.parentElement.style.display = 'none';
        });
    });

});