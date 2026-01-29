JAZZMIN_SETTINGS = {
    "site_title": "AccShop",
    "site_header": "Hệ Thống Quản Lý Tài Khoản Game",
    "site_brand": "AccShop",
    "welcome_sign": "Chào Mừng Đến Với Hệ Thống Quản Lý Tài Khoản Game",
    "copyright": "© 2025 AccShop",

    "site_logo": "images/console.png",
    "login_logo": "images/console.png",
    
    "logo_icon": "images/icon.png", 
    "site_icon": "images/icon.png",

    "topmenu_links": [
        {"name": "Trang Chủ", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Website", "url": "/", "new_window": True},
    ],
    
    "order_with_respect_to": [ 
        "auth", 
        "accounts"
    ],
    
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
}
