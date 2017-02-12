#python
from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "Yueer_PSS.py",
            "icon_resources": [(1, "icon.ico")]
        },
        {
            "script": "Purchase.py"
        },
        {
            "script": "Sell.py"
        },
        {
            "script": "SearchGoods.py"
        },
        {
            "script": "Modify.py"
        },
        {
            "script": "About.py"
        },
        {
            "script": "Statement.py"
        },
        {
            "script": "Main.py"
        },
        {
            "script": "Update.py"
        },
        {
            "script": "QuerySell.py"
        },
    ],
    data_files=["icon.ico","database.dat","statement.dat","Account.dat","delete.bmp","edit.bmp","Out.bmp","search.bmp","searchall.bmp"]
)
