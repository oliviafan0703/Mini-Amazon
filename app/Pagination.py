class Pagination:
    def get_pagination_values(current_page, max_pages):
                #show 5 pages 
        #total pages = math.ceil([TOTAL ITEMS ON THIS PAGE]/ROWS_PER_PAGE)
        # print(totalPages)
        maxDisplayedPages = min(max_pages,5)
        if(current_page > max_pages):
            current_page = max_pages
        pages = [current_page]
        generated_pages = 1
        
        current_direction = 1
        while generated_pages<maxDisplayedPages:

            if current_direction == 1:
                #if generating to the back 
                if(pages[-1]+1<=max_pages):
                    pages.append(pages[-1]+1)
                    generated_pages+=1
            else:
                if pages[0]-1>=1:
                    pages.insert(0,pages[0]-1)
                    generated_pages+=1

            current_direction*=-1
        return pages
