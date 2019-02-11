from obscureridge import read_string_from_file

############################################################

def test_obscureridge():

    print("testing obscureridge")

    assert read_string_from_file(None, "default") == "default"

############################################################
