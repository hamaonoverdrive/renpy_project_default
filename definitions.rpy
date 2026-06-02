# ==== UI SFX ====

# sound for hovering on a button
define audio.ui_hover = None
# sound for clicking on a button
define audio.ui_click = None
# sound for advancing text
define audio.ui_adv = None

# ==== NAVIGATION ====
transform hover_nav:
    # applied to all navigation menu items, intended for hover effects
    #on hover:
        #stuff
    on idle:
        # restore default
        matrixcolor IdentityMatrix()

