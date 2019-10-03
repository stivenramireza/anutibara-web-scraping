def paginate_properties(pages_list_to_process):
    for i in range(1, 839):
        pages_list_to_process.append('https://www.fincaraiz.com.co/finca-raiz/venta/medellin/?ad=30|'+ str(i) +'||||1||8,9,3,4,22,2,5,7,19,23,21,18,20|||55|5500006||||||||||||||||1|||1||griddate%20desc||||-1||')
    return pages_list_to_process

def main():
    pages_list = []
    pages_list = paginate_properties(pages_list)

if __name__ == "__main__":
    main()