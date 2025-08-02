import xml.etree.ElementTree as ET
import zipfile
import os

def build_qti_zip(questions, filename="canvas_quiz"):
    root = ET.Element('questestinterop')
    assessment = ET.SubElement(root, 'assessment', attrib={'title': filename, 'ident': 'quiz1'})
    section = ET.SubElement(assessment, 'section', attrib={'ident': 'root_section'})

    for i, q in enumerate(questions, 1):
        item = ET.SubElement(section, 'item', attrib={'ident': f'q{i}', 'title': f'Question {i}'})
        pres = ET.SubElement(item, 'presentation')
        mat = ET.SubElement(pres, 'material')
        ET.SubElement(mat, 'mattext').text = q['question']
        rlid = ET.SubElement(pres, 'response_lid', attrib={'ident': f'resp{i}', 'rcardinality': 'Single'})
        rc = ET.SubElement(rlid, 'render_choice')
        for ident, text in q['answers']:
            label = ET.SubElement(rc, 'response_label', attrib={'ident': ident})
            mat = ET.SubElement(label, 'material')
            ET.SubElement(mat, 'mattext').text = text

        proc = ET.SubElement(item, 'resprocessing')
        out = ET.SubElement(proc, 'outcomes')
        ET.SubElement(out, 'decvar', attrib={'vartype': 'Decimal', 'defaultval': '0'})
        cond = ET.SubElement(proc, 'respcondition', attrib={'continue': 'No'})
        cv = ET.SubElement(cond, 'conditionvar')
        ET.SubElement(cv, 'varequal', attrib={'respident': f'resp{i}'}).text = q['correct']
        ET.SubElement(cond, 'setvar', attrib={'action': 'Set'}).text = '100'

    xml_path = f"{filename}.qti.xml"
    zip_path = f"{filename}.zip"
    ET.ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)

    with open("imsmanifest.xml", "w") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="man1" xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1 
http://www.imsglobal.org/xsd/imscp_v1p1.xsd">
<resources>
<resource identifier="res1" type="imsqti_xmlv1p2" href="{xml_path}">
<file href="{xml_path}"/>
</resource>
</resources>
</manifest>""")

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(xml_path)
        zipf.write("imsmanifest.xml")

    return zip_path
