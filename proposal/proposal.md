# Problem description

# Background on project 8 (supplied by collaborators)

## Regionalization.ino
This code is designed to display Lao-language fonts on screens using bytecode font file
Task 8 lao regionalization of lora module
 - Requirement : displaying a lao messages on the HTCC AB02S OLED.
 - Deliverables : either: a bytecode PROGMEM corresponding to a predetermined set of lao messages, or a fully-fledged bytecode font file
     ໃນ task 8  ນີ້ຂ້າພະເຈົ້າເອງໄດ້ຖືກມອບໝາຍໃຫ້ເຮັດ BYTECODE ສຳລັບພາສາລາວເພື່ອສະແດງຢູ່ໃນຈໍ HTCC AB02S OLED, E-paper module ເຊິ່ງເລີ່ມຕົ້ນ project ນີ້ມາຂ້າພະເຈົ້າເອງກໍໄດ້ມີການໄປສຶກສາກ່ຽວກັບເລື່ອງຕ່າງໆທີ່ກ່ຽວຂ້ອງບໍ່ວ່າຈະເປັນ Bytecode, ASCII, unicode, Bitmaps, HEX code, Binary code ແລະ ອັກສອນລາວພື້ນຖານ. ເຊິ່ງບັນຫາທຳອິດທີ່ໄດ້ພົບເຈີແມ່ນເຄື່ອງມຶ AI ຕ່າງໆບໍ່ສາມາດແປງຈາກຂໍ້ຄວາມອັກສອນລາວໄປເປັນ HEX code ຫຼື binary code ເພື່ອສະແດງເທິງໜ້າຈໍໂດຍກົງໄດ້ເຮັດໃຫ້ຕ້ອງໄດ້ມີການສຶກສາການເຮັດວຽກຂອງ E-paper module ແລະ ການເຮັດ binary code ໄປເປັນ HEX code ເພື່ອໃຫ້ສະແດງເທິງໜ້າຈໍຂອງ E-paper module. ເຊິ່ງຫຼັກການເຮັດວຽກຂອງມັນກະຄືຈະຮັບຄ່າທີ່ເປັນ Hex code ໄປແປງເປັນ binary code ເພື່ອສະແດງເທິງໜ້າຈໍເຊິ່ງຈະກຳນົດຂະໜາດ px ຕາມເລກ 1 = 1px ຂອງໂຕອັກສອນພາສາລາວ ເຊິ່ງຂະໜາດເຕັມຂອງໂຕອັກສອນແມ່ນ 24x16 px (Height x Width). ຫຼັງຈາກເລີ່ມເຮັດໂຕອັກສອນລາວໄປໄດ້ໄລຍະໜຶ່ງທາງເຮົາເອງກໍໄດ້ພົບອີກບັນຫາໜຶ່ງຄືບັນດາສະຫຼະ ແລະ ວັນນະຍຸກໃນພາສາລາວບາງໂຕທີ່ໄດ້ມີການໃຊ້ຢູ່ທາງເທິງ​ຫຼື ລຸ່ມຂອງໂຕອັກສອນລາວເວລາພິມເຂົ້າກັບໂຕອັກສອນມັນຈະເພີ່ມໄລຍະຫ່າງມາເອງ（ຕົວຢ່າງ: ດ ີ , ຄ ູ, ບ ໍ ່ ) ທາງເຮົາເອງເລີຍໄດ້ມີການແກ້ໄຂໃຫ້ປຸ່ມກົດບາງໂຕຈະພິມອອກມາເປັນຄຳເວົ້າໃນພາສາລາວທີ່ໄດ້ມີການໃຊ້ອັກສອນພິເສດເຫຼົ່ານັ້ນ ( F = ດີ ) ແລະ ເນື່ອງຈາກຈຳນວນຂອງຄີບອດມີຈຳກັດຂ້າພະເຈົ້າເລີຍຕ້ອງໄດ້ໃສ່ສະເພາະຄຳເວົ້າທີ່ໄດ້ໃຊ້ປະຈຳມາໃສ່ໃນຄີບອດເທົ່ານັ້ນ ແລະ ຂ້າພະເຈົ້າເອງກໍໄດ້ອອກແບບແປ້ນພິມພາສາລາວຂຶ້ນມາໃໝ່.

   In this task 8, I myself was assigned to make BYTECODE for Lao language to be displayed on HTCC AB02S OLED screen, E-paper module which started this project. The first problem encountered is that the AI machines cannot convert Lao text to HEX code or binary code to display on the screen directly, so it is necessary to study the operation of the E-paper module and make the binary code to HEX code to display on the screen of the E-paper module. Its main function is to receive the Hex code and convert it to a binary code to display on the screen which will determine the px size according to the number 1 = 1px of the Lao letter, the full size of the letter is 24x16 px (Height x Width). After starting to write Lao characters for a while, we found another problem, some letters and words in the Lao language that have "accent" marks above or below the letter (Lao characters), when typing the letters, it will increase the spacing between the letters (for example:ດ ີ , ຄ ູ, ບ ໍ ່ ). We have solved it so that some keys on a specially designed keyboard will print out entire words that have those special characters as example, F = ດີ and because the number of keys on a keyboard is limited, I have added Only frequently used words to the keyboard and I myself have redesigned the Lao keyboard.

Brief overview of the problem, context and engineering approach to tackle the problem.

# Presentation of the proposal

Technical aspects may be described here.

# Assessment of the quality of the proposal

Evaluate its value in the context of the project. What will it solve, is it safe, etc. Check Lara’s slides for what to cover.


