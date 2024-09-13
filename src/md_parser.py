class MD_Parser:
    bold_regex = '(?P<delim>\*\*)(?P<delim_text>(\w\s*)+\w)(?P=delim)'

    def __init__(self, delimitter, text_type="text"):
        self.delimitter = delimitter
        self.text_type = text_type

    def parse(self, text):
        print("\nCalled parse()\n")
        chunks = []

        delim = self.delimitter
        len_delim = len(delim)
        text_type = self.text_type
        
        i, j = 0, 0
        loop_count = 0
        
        while j + len_delim <= len(text):
            loop_count += 1
            if loop_count > len(text):
                break
                e = f"\n\tInfinite Loop:\n\t\ti = {i}\n\t\tj = {j}"
                raise Exception(e)

            check = text[j:j+len_delim]
            
            if check == delim:
                # validate delim
                k = j+len_delim
                if k + len_delim > len(text):
                    j += 1
                    continue
                
                next_step = text[k:k+len_delim]

                print(f"next_step = {next_step.__repr__()}\n")
                if next_step == '':
                    j += 1
                    print(f"\ni: {i}\nj: {j}")
                    continue
                if next_step == delim:
                    # invalid, advance by len_delim
                    j = k
                    continue
                elif next_step[0] == ' ' or next_step[0] == '*':
                    # invalid, advance by 1, repeat check
                    j += 1
                    continue
                else:
                    while k + len_delim <= len(text):
                        k += 1
                        closer = text[k:k+len_delim]
                        if closer == delim:
                            # valid closer
                            print(f"text[k-1] -> {text[k-1]}")
                            if text[k-1] == ' ' or text[k-1] == '*':
                                # invalid, continue to next iteration
                                continue
                            else:
                                # valid
                                # `k` now points to first position of closing delimitter
                                # `j` now points to first position of open delimitter
                                # if i < j then text[i:j] is text node
                                if i < j:
                                    chunk = (text[i:j], "text")
                                    chunks.append(chunk)

                                # and text[j+len_delim:k] is text_type node
                                chunk = (text[j+len_delim:k], text_type)
                                chunks.append(chunk)

                                # move `i` and `j` to `k + len_delim`
                                i = k + len_delim
                                j = i

                                # if end-of-string:
                                ### if i < j: text[i:] is text node
                    else:
                        print("End of String while searching for closer:")
                        print(f"\ni: {i}\nj: {j}\nk: {k}")
                        print(f"text[i:] => {text[i:]}")
                        if i < k:
                            chunks.append((text[i:], "text"))
                        i = j
                        break
        else:
            print(f"End of string while searching for opener:")
            print(f"\ni: {i}\nj: {j}\n")
            if i < len(text):
                chunks.append((text[i:], "text"))

                    # `j' now points to the first position of a potential open delimitter
                    # We need to scan forward from here for a either:
                    ### 1. Closing delimitter
                    ###### - `j' now points to first position of valid open delimitter
                    ###### - `k' now points to first position of valid closing delimitter
                    ### 2. End of string
                    ###### - We find no closing delimitter, therefore `j' is invalid
                

        print("The finale...")
        print(f"i: {i}\nj: {j}\n")
        if len(chunks) == 0:
            chunks.append((text[i:], "text"))
        return chunks


text = "This is a **bold** word."

def split_nodes_delimiter(t, delimitter):
    len_delim = len(delimitter)
    bounds = []
    for i, _ in enumerate(t):
        if t[i:i+len_delim] == delimitter:
           bounds.append((i, i+len_delim)) 
    return bounds

def _snd(t, delim, text_type):
    len_delim = len(delim)
    types = []

    i = 0
    j = 0

    def find_next_delimiter(t, delim, i, j):
        while i < len(t):
            if t[i:i+len(delim)] == delim:
                if t[i-len(delim):i] != delim:
                    if not t[i-1].isspace():
                        return True, j, i
            i += 1
        return False, j, i


    while i < len(t):
        if t[i:i+len_delim] == delim:
            if ( i + len_delim ) < len(t):
                x = i+len_delim
                if t[x].isspace():
                    x += 1
                    i = x
                if t[x:x+len_delim] == delim:
                    i = x
                    x += 1

                found, j2, i2 = find_next_delimiter(t, delim, i+len_delim, i+len_delim)


                if found:
                    if i > j:
                        print(f"\ni: {i}\nj: {j}")
                        types.append((t[j:i], "text"))
                    types.append((t[j2:i2], "bold"))
                    j = i2+len_delim
                    i = j
                else:
                    types.append((t[j:i], "text"))
                    i += 1
        i += 1

        #     while x < len(t):
        #         if t[x:x+len_delim] == delim:
        #             if t[x-1].isspace():
        #                 x = x+len_delim
        #                 i = x
                        
        #             if x - i > 1:
        #                 if j > 0:
        #                     types.append((t[:i], "text"))
        #                 types.append((t[i+len_delim:x], text_type))
        #             i = x+len_delim
        #             j = i
        #         x += 1
        # i += 1
        # hmmm
        
    
    if j < len(t) and i > j:
        types.append((t[j:i], "text"))
    

    return types

t = _snd(text, "**", "bold")
t2 = _snd("****", "**", "bold")
t3 = _snd("**a**", "**", "bold")
t5 = _snd("****b**", "*", "bold")

def show(text, d):
    print(f"\ntext: \"{text}\", delim: \"{d}\"\nt: {_snd(text, d, 'bold')}")

show(text, "**")
show("**b**", "*")
show("****", "**")
show("**a**", "**")
show("****b**", "*")
show("****b***", "*")

print()