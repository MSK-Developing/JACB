class Config():
    # <-----------------> OPZIONI GENERALI <----------------->
    # Opzione per caricare il token da un file ("token") o dal config.
    # Settare a nullo (o tutto il resto) per caricare il token dal Config
    TOKEN_METHOD="DEV"
    # Il token del bot
    BOT_TOKEN=""
    # L'ID Del Server Dove il Bot sarà inserito
    GUILD_ID=000000000000000000

    # <-----------------> COLORI <----------------->
    
    # Colore dei rispettivi Embed, offre due opzioni per la personalizzazione:
    #       - Colori Preimpostati, sono "rosso, giallo, verde, blu" e vengono 
    #          settati in questo modo: colore_embed_successo = "rosso"
    #       - Colori Personalizzati: Sono colori in HEX: colore_embed_successo = 0xff0000
    #          Color Picker: https://g.co/kgs/5jMBgu
    colore_embed_successo = 0000000
    colore_embed_fallimento = 0000000

    # <-----------------> MESSAGGI <----------------->
    lang = {
        "GEN_COUPON_COMMAND_DESCRIPTION": "Generates a Coupon with a given discount",
        "GEN_COUPON_EMBED_TITLE": "Coupon Created!",
        "DELETE_COUPON_COMMAND_DESCRIPTION": "Delete a Coupon",
        "DELETE_COUPON_EMBED_TITLE": "Coupon Deleated!",
        "USE_COUPON_COMMAND_DESCTRIPTION": "Use a Cuopon",
        "USE_COUPON_COMMAND_SUCCESS_EMBED_TITLE": "Coupon Used Succefluly!",
        "USE_COUPON_COMMAND_FAILED_EMBED_TITLE": "This cuopun is Invalid!",
        "CHECK_COUPON_COMMAND_DESCRIPTION": "Checks if a Coupon is valid or Invalid",
        "CHECK_COUPON_COMMAND_SUCCESS_EMBED_TITLE": "Coupon Exist!",
        "CHECK_COUPON_COMMAND_FAILED_EMBED_TITLE": "This cuopun is FAKE!",
        "CHECK_COUPON_COMMAND_SUCCESS_EMBED_DESCRIPTION": ":ok_hand: :man_police_officer: Yay :)",
        "CHECK_COUPON_COMMAND_FAILED_EMBED_DESCRIPTION": ":punch: :police_car: Not cool :("
    }
