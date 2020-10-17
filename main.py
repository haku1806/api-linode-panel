import instances

if __name__ == "__main__":
    
    print("Chao mung den voi Panel HAKU VPS")
    API = input("Nhap API xac thuc cua ban: ")
    linode = instances.Instances(API)
    while (True):
        print("\n----------------------------------------------------------------------------------------------------------")
        print("API cua ban la : {}".format(API))
        print('1. Kiem tra cac VPS hien tai')
        print('2. Khoi dong VPS. ')
        print('3. Khoi dong lai VPS')
        print('4. Tat VPS')
        print('5. Xoa VPS')
        print('6. Rescue VPS')
        print('7. Clone VPS')
        print('8. Get config ID')
        print('0. Exit\n')
        inputKeyboard = int(input('Nhap lua chon cua ban: '))
        print()
        if inputKeyboard == 1:
            print()
            linode.printListLinodes()
        # print(getInfoListVPS())
        elif inputKeyboard == 2:
            # 1: boot VPS
            linode.selectTypeBoot(1)
        elif inputKeyboard == 3:
            # 2: reboot VPS
            linode.selectTypeBoot(2)
        elif inputKeyboard == 4:
            # 3: shutdown VPS
            linode.selectTypeBoot(3)
        elif inputKeyboard == 5:
            # 4: shutdown VPS
            linode.selectTypeBoot(4)
        elif inputKeyboard == 6:
            # 5: rescue VPS
            linode.selectTypeBoot(5)
        elif inputKeyboard == 7:
            # menuCloneVPS()
            linode.menuCloneLinode()
            pass
        elif inputKeyboard == 8:
            linode.menuGetInfoDiskConfigLinode()
            # print(linode.getListDisk(20377958))

        elif inputKeyboard == 0:
            exit()
        else:
            print('Chon sai, Vui long nhap lai')