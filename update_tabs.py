def refactor_tabs():
    filepath = "/Users/aquib/Downloads/GraminAI/app.py"
    with open(filepath, "r") as f:
        lines = f.readlines()

    new_lines = []
    in_tab_block = False
    
    tab_identifiers = [
        "with tab1:", "with tab2:", "with tab3:", 
        "with tab4:", "with tab5:", "with tab6:", "with tab7:"
    ]

    for line in lines:
        stripped_line = line.strip()
        
        # Check if line initiates a tab block
        if any(stripped_line == t for t in tab_identifiers):
            new_lines.append(line)
            # Add container right after the tab
            indent = line[:len(line) - len(line.lstrip())]
            new_lines.append(f"{indent}    with st.container(border=True):\n")
            in_tab_block = True
            continue
            
        if in_tab_block:
            # If line is completely empty, just append empty
            if not stripped_line:
                new_lines.append(line)
                continue
                
            line_indent = len(line) - len(line.lstrip())
            
            # If indentation is 0 or it's un-indented back to root level, we exit tab block
            if line_indent == 0 and not line.startswith(" "):
                in_tab_block = False
                new_lines.append(line)
            else:
                # Add 4 spaces for the new with st.container(border=True): block
                new_lines.append("    " + line)
        else:
            new_lines.append(line)

    with open(filepath, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    refactor_tabs()
    print("Successfully refactored tabs.")
