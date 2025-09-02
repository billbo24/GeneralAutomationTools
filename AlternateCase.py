

#%%
def alternate_case(s):
    result = ""
    upper = False  # Start with lowercase
    for char in s:
        if char.isalpha():
            if upper:
                result += char.upper()
            else:
                result += char.lower()
            upper = not upper
        else:
            result += char  # Keep non-alphabet characters as is
    return result

# Example usage
#a = alternate_case("hey guys what'going on?")
#print(a)
# %%
