def show_map(current_room):
    print("\n--- CAVE MAP ---")
    if current_room == "Armory":
        print("      [X Armory ]")
        print("          |     ")
        print("      [ Search Room ]")
        print("          |     ")
        print("      [ Hallway ]")
        print("          |     ")
        print("      [ Entrance ] -- [ King's Room ]")
        
    elif current_room == "The Search Room":
        print("      [ Armory ]")
        print("          |     ")
        print("      [X Search Room ]")
        print("          |     ")
        print("      [ Hallway ]")
        print("          |     ")
        print("      [ Entrance ] -- [ King's Room ]")
        
    elif current_room == "Dark Hallway":
        print("      [ Armory ]")
        print("          |     ")
        print("      [ Search Room ]")
        print("          |     ")
        print("      [X Hallway ]")
        print("          |     ")
        print("      [ Entrance ] -- [ King's Room ]")
        
    elif current_room == "Entrance":
        print("      [ Armory ]")
        print("          |     ")
        print("      [ Search Room ]")
        print("          |     ")
        print("      [ Hallway ]")
        print("          |     ")
        print("      [X Entrance ] -- [ King's Room ]")
        
    elif current_room == "THE KINGS ROOM":
        print("      [ Armory ]")
        print("          |     ")
        print("      [ Search Room ]")
        print("          |     ")
        print("      [ Hallway ]")
        print("          |     ")
        print("      [ Entrance ] -- [X King's Room ]")
    print("----------------\n")