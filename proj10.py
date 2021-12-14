 #############################################################################
 # Solitaire: Scorpion
 #
 # project header 
 # __________________________
 #
 # sets the menu 
 # def initialize :
 #     deals to the tableau, sets the foundation and stock 
 # def deal tableau :
 #     deals to the tableau 
 # def deal from stock :
 #     deals the three cards left over from the stock 
 # def display :
 #     displays the stock, foundation, and tableau 
 # def validate move: 
 #     check to see if a move is valid 
 # def move :
 #     moves the cards if move is valid 
 # def check sequence :
 #     checks to see if a column of the tableau if complete 
 # def move to foundation :
 #     moves comoleted columns to the foundation 
 # def check for win :
 #     checks to see if the foundation is full 
 # def get option :
 #     gets the menu option from the user 
 # def main :
 #     calls all the above function 
 #     prints the menu, tableau 
 #     prints error messages for invalid moves 
 # call the main function 
 # 
 ############################################################################


#DO NOT DELETE THESE LINES
import cards, random
random.seed(100) #random number generator will always generate 
                 #the same random number (needed to replicate tests)

MENU = '''     
Input options:
    D: Deal to the Tableau (one card to first three columns).
    M c r d: Move card from Tableau (column,row) to end of column d.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def initialize():
    '''
    does not take any arguments 
    returns a tupple of the tableau, stock, and foundation 
    
    deals the cards 
    outs them in teh appropriate areas 
    '''
    
    #initialize the foundation 
    foundation = [ [],[],[],[] ] 

    #initialize the stock 
    stock = cards.Deck()
    stock.shuffle()
    
     #initialize the tableau 
    tableau = [ [], [], [], [], [], [], []]
    final_tableau = deal_tableau(stock, tableau)
    
    tup = (stock, final_tableau, foundation)
    return tup 

def deal_tableau(stock,tableau):
    '''
    takes the tablea and the stock as an argument 
    returns the dealt tableau 
    
    deals the cards from the stock to the tableau 
    '''
    
    #deals 49 cards 
    cards_dealt = 0 
    while cards_dealt != 49:
        for col in tableau: 
            card = stock.deal()
            col.append(card)
            cards_dealt += 1 
    
    #flips the first three cards of the first three rows 
    for i in range(3):
        for o in range(3) :
            tableau[i][o].flip_card()

    return tableau

def deal_from_stock(stock, tableau):
    
    '''
    takes the stock and the tableau as arguments 
    returns nothing 
    
    deals the three cards from the stock to the first three 
    columns of the tableau 
    '''
    
    #create a list of the cards in the stock 
    stock_list = [] 
    for c in range(len(stock)): 
        card = stock.deal() 
        stock_list.append(card) 
    
    #deal the cards in the stock to the tableau 
    tab_index = 0 
    for crd in stock_list: 
        tableau[tab_index].append(crd)
        tab_index += 1 
  
def display(stock, tableau, foundation):
    '''Display the stock and foundation at the top.
       Display the tableau below.'''
       
    print("\n{:<8s}{:s}".format( "stock", "foundation"))
    if stock.is_empty():
        print("{}{}".format( " ", " "),end='') # fill space where stock would be so foundation gets printed in the right place
    else:
        print("{}{}".format( " X", "X"),end='')  # print as if face-down
    for f in foundation:
        if f:
            print(f[0],end=' ')  # print first card in stack(list) on foundation
        else:
            print("{}{}".format( " ", " "),end='') # fill space where card would be so foundation gets printed in the right place
            
    print()
    print("\ntableau")
    print("   ",end=' ')
    for i in range(1,8):
        print("{:>2d} ".format(i),end=' ')
    print()
    # determine the number of rows in the longest column        
    max_col = max([len(i) for i in tableau])
    for row in range(max_col):
        print("{:>2d}".format(row+1),end=' ')
        for col in range(7):
            # check that a card exists before trying to print it
            if row < len(tableau[col]):
                print(tableau[col][row],end=' ')
            else:
                print("   ",end=' ')
        print()  # carriage return at the end of each row
    print()  # carriage return after printing the whole tableau
 
def validate_move(tableau,src_col,src_row,dst_col):
    '''
    takes the tableau, source column, source row, and destination column
    as arguments 
    returns a boolean, true if valid, false if invalid 

    '''
    
    #finds the column and the card the user wants to move to
    move_list = tableau[src_col] 
    
    error = False 
    try:
        move_card = move_list[src_row] 
    except:
        move_card = tableau[0][0] 
        error == True 
        pass
    
    #finds the column the user wants to move to 
    to_list = tableau[dst_col]
 
    if error == True: 
        move = 'invalid'
        
    #king to empty col is valud  
    elif len(to_list) == 0:
        if move_card.rank() == 13:
            move = 'valid'
        else: 
            move = 'invalid'
    else: 
        to_card = to_list[-1] #finds the card the user wants to move to 
        if to_card.suit() == move_card.suit():
            if to_card.rank() == move_card.rank() + 1 :
                move = 'valid'
            else: 
                move = 'invalid'
        else:
            move = 'invalid'
            
    if move == 'valid': 
        return True 
    else: 
        return False 
        
    
def move(tableau,src_col,src_row,dst_col):
    '''
    takes the tableau, source column, source row, and desitnation column 
    as arguments 
    returns a boolea, true if move is complete, false if incomplete 
    
    calls the valudate move function 
    '''
    
    #validate the move 
    boo = validate_move(tableau, src_col, src_row, dst_col)
    
    #move cards if valid move 
    if boo == True: 
        
        #finds the column and the card the user wants to move to
        move_list = tableau[src_col] 
        move_card = move_list[src_row] 
        
        #finds the column the user wants to move to 
        to_list = tableau[dst_col]
        move_index = move_list.index(move_card)
        move_list = move_list[move_index:]
        
        tableau[dst_col].extend(move_list)
        tableau [src_col] = tableau [src_col] [:move_index]
        
        #flips card if face down card is at bottom of column 
        for col in tableau: 
            if len(col) != 0: 
                if not col[-1].is_face_up():
                    col[-1].flip_card()
                    
        return True 
    
    else: 
        return False 
    
def check_sequence(column_lst):
    '''
    take a column of the tableau as argument 
    reutns a boolean, true if sequence is complete, false if incomplete 
    '''

    #checks if column is complete 
    if len(column_lst) == 13: 
        if column_lst[0].rank() == 13 and column_lst[12].rank()== 1:
            king_suit = column_lst[0].suit()
            test_list = []
            for card in column_lst:
                #adds cards to test list 
                if card.suit() == king_suit:
                    test_list.append(True)
                else: 
                    test_list.append(False)
                    
            #tests the contents of the test list 
            if False in test_list:
                return False 
            else: 
                return True 
                    
        else:
            return False
    else: 
        return False
            
    
def move_to_foundation(tableau,foundation):
    '''
    takes the tableau and the foundation as arguments 
    returns nothing 
    
    moves completed columns to the foundation 
    calls the check sequence function 
    '''
    
    for col in tableau:
        #checks to see if each column is complete 
        sequence_bool = check_sequence(col) 
        if sequence_bool == True:
            for i in range(len(foundation)): 
                if len(foundation[i]) == 0: 
                    for card in col: 
                        #adds teh column to the foundation 
                        foundation[i].append(card)
                    #clears the column in the foundation 
                    col.clear()
                else:
                    pass
                  
def check_for_win(foundation):
    '''
    takes the foundation as an argument 
    returns a boolean, true if gamne is won, false if game is lost
    '''
    
    win_list = [] 
    for stack in foundation: 
        if len(stack) == 13:
            win_list.append(True) 
        else: 
            win_list.append(False)
            
    if False in win_list:
        return False
    else: 
        return True 
        

def get_option():
    '''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    D: Deal to the Tableau (one card to first three columns).
    M c r d: Move card from Tableau column,row to end of column d.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
    '''
    option = input( "\nInput an option (DMRHQ): " )
    option_list = option.strip().split()
    
    opt_char = option_list[0].upper()
    
    if opt_char in 'DRHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'M' and len(option_list) == 4 and option_list[1].isdigit() \
        and option_list[2].isdigit() and option_list[3].isdigit():
        return ['M',int(option_list[1]),int(option_list[2]),int(option_list[3])]

    print("Error in option:", option)
    return None   # none of the above
 
def main():
    '''
    takes no arguemnts 
    returns nothing 
    
    calls all the functions
    tests the user input 
    prints errors 
    '''

    print("\nWelcome to Scorpion Solitaire.\n")

    stock, tableau, foundation = initialize()

    display(stock, tableau, foundation)
    print(MENU)
    option_lst = get_option()
    
    while option_lst and option_lst[0] != 'Q':
        
        #if user wants to move 
        if option_lst[0] == 'M':
            
            #chnage the human numbers into indicies
            option_lst[1] = option_lst[1] - 1 
            option_lst[2] = option_lst[2] - 1
            option_lst[3] = option_lst[3] - 1
      
            #call the move function  
            win_bool = False
            move_bool = move(tableau, option_lst[1], option_lst[2], option_lst[3])
            if move_bool == True: 
                for col in tableau:
                    #checks to see if each column is complete 
                    sequence_bool = check_sequence(col) 
                    if sequence_bool == True: 
                        #moves completed columns to foundation 
                        move_to_foundation(tableau, foundation)
                        #checks if foundation is full 
                        win_bool = check_for_win(foundation)
                        if win_bool == True:
                            print('You won!')
                            print('\nNew Game.')
                            stock, tableau, foundation = initialize()

                    
                display(stock, tableau, foundation)
                if win_bool == True: 
                    #prints the menu again if the game is won 
                    print(MENU)
                
            else: 
                print("Error in move:",option_lst[0],",",option_lst[1]+ 1,",",option_lst[2] + 1,",",option_lst[3]+ 1)
                
        elif option_lst[0] == 'D':
            deal_from_stock(stock, tableau)
            display(stock, tableau, foundation)
            
        elif option_lst[0] == 'H':
            print(MENU)
        
        elif option_lst[0] == 'R':
            stock, tableau, foundation = initialize()
            display(stock, tableau, foundation)
            print(MENU)
            
            
        option_lst = get_option()
    
    print("Thank you for playing.") 

if __name__ == '__main__':
    main() 
