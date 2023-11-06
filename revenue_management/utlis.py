import frappe
import traceback
import sys
from frappe.core.doctype.data_import.data_import import start_import


def dataimport(file=None, import_type=None, reference_doctype=None):
    try:
        doc = {
                "doctype": "Data Import",
                "reference_doctype": reference_doctype,
                "import_type": "Insert New Records",
                "status": "Pending"
            }
        data = frappe.get_doc(doc)
        data.insert()
        frappe.db.commit()
        frappe.db.set_value("Data Import", data.name, "import_file", file)
        frappe.db.commit()
        data_import = data.name
        start_import = start_import(data_import)
        return {"success": True}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("dataimport", "line No:{}\n{}".format(
            exc_tb.tb_lineno, traceback.format_exc()))
        return {"success": False, "error": str(e)}
