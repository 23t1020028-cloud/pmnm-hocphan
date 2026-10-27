import re
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
)


class RegisterForm(FlaskForm):
    # Tên đăng nhập: bắt buộc, 4-20 ký tự, chỉ chữ thường không dấu, số, _; không trùng tên đã có
    username = StringField(
        "Tên đăng nhập",
        validators=[
            DataRequired(message="Vui lòng nhập tên đăng nhập."),
            Length(
                min=4,
                max=20,
                message="Tên đăng nhập phải từ 4 đến 20 ký tự.",
            ),
        ],
    )

    # Email: bắt buộc, đúng định dạng
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Vui lòng nhập email."),
            Email(message="Email không đúng định dạng."),
        ],
    )

    # Mật khẩu: tối thiểu 8 ký tự
    password = PasswordField(
        "Mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập mật khẩu."),
            Length(
                min=8, message="Mật khẩu phải chứa ít nhất 8 ký tự."
            ),
        ],
    )

    # Nhập lại mật khẩu: trùng mật khẩu
    confirm_password = PasswordField(
        "Nhập lại mật khẩu",
        validators=[
            DataRequired(message="Vui lòng nhập lại mật khẩu."),
            EqualTo("password", message="Mật khẩu nhập lại không khớp."),
        ],
    )

    # Đồng ý điều khoản: bắt buộc tích
    agree_terms = BooleanField(
        "Đồng ý điều khoản dịch vụ",
        validators=[
            DataRequired(message="Bạn phải đồng ý với điều khoản.")
        ],
    )

    submit = SubmitField("Đăng ký")

    def __init__(self, users_dict=None, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.users_dict = users_dict or {}

    # Custom Validator kiểm tra ký tự hợp lệ (chỉ chữ thường không dấu, số, _)
    def validate_username(self, field):
        pattern = r"^[a-z0-9_]+$"
        if not re.match(pattern, field.data):
            raise ValidationError(
                "Tên đăng nhập chỉ được chứa chữ cái thường không dấu, chữ số và dấu gạch dưới (_)."
            )

        # Kiểm tra không trùng tên đã có trong USERS
        if field.data in self.users_dict:
            raise ValidationError("Tên đăng nhập đã được sử dụng.")