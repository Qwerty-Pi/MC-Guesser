paddlex --pipeline OCR \
        --input artifact/paper-2/2025/page/5.png \
        --use_doc_orientation_classify False \
        --use_doc_unwarping False \
        --use_textline_orientation False \
        --save_path ./output \
        --device cpu