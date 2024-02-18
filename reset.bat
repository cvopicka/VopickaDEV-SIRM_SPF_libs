pip uninstall -y sirm_spf_libs
python setup.py bdist_wheel
pip install ".\dist\sirm_spf_libs-2024.217.1248a0-py3-none-any.whl"