from ttkthemes import ThemedStyle

def aplicar_tema(root):
    style = ThemedStyle(root)
    style.set_theme("arc")  # Alternativa: "radiance", "breeze", "equilux"
