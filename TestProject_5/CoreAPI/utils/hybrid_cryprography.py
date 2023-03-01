import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from ..models import StorageEncode, StorageDecode
from .constants import path_to_hidden_file, path_to_cover_file, path_to_encoded_file, path_to_decoded_file
import base64
from .steganography_file.image_module import commands as image_commands
from .steganography_file.audio import commands as audio_commands
from .steganography_file.video import commands as video_commands


def encode_file(hidden_file, public_key, user_id, storage_id, cover_file_type, cover_file):
    """
    Encrypts a file using AES encryption and a randomly generated key, then
    encrypts the key with RSA encryption and saves the encrypted file and key
    to disk. Updates the corresponding StorageEncode object with the path to
    the encrypted file and the encrypted key.

    Args:
        hidden_file (File): The file to be encrypted.
        public_key (str): The public key to use for RSA encryption.
        user_id (int): The ID of the user who owns the file.
        storage_id (int): The ID of the corresponding StorageEncode object.

    Returns:
        None
    """
    filename = hidden_file.name.split('/')[-1]
    print(filename)
    cover_file_name = cover_file.name.split('/')[-1]
    print(cover_file_name)
    print(user_id)
    with open(path_to_hidden_file(user_id, filename), 'rb') as f:
        data = f.read()
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        file_out = open(path_to_encoded_file(user_id, filename), "wb")
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
        file_out.close()

        encrypted_password = rsa.encrypt(
            key, rsa.PublicKey.load_pkcs1(public_key))
        print("enc: ", encrypted_password)
        encoded = base64.b64encode(encrypted_password).decode()
        StorageEncode.objects.filter(id=storage_id).update(
            encrypted_password=encoded)

        i = open(path_to_encoded_file(user_id, filename), 'rb+')
        print(i)
        i.close()
        StorageEncode.objects.filter(id=storage_id).update(
            encoded_file=path_to_encoded_file(user_id, filename))

        print(cover_file_type)
        if cover_file_type == 'A':
            args_dictionary = {
                'input_file': path_to_cover_file(user_id, cover_file_name),
                'output_file': path_to_encoded_file(user_id, replace_file_extension(filename, 'wav')),
                'message_file': path_to_encoded_file(user_id, filename),
                'operation': 'encode',
                'user_id': user_id,
                'storage_id': storage_id,
            }
            audio_commands.main(args_dictionary)
        elif cover_file_type == 'I':
            args_dictionary = {
                'input_file': path_to_cover_file(user_id, cover_file_name),
                'output_file': path_to_encoded_file(user_id, replace_file_extension(filename, 'png')),
                'message_file': path_to_encoded_file(user_id, filename),
                'operation': 'encode',
                'user_id': user_id,
                'storage_id': storage_id,
            }
            image_commands.main(args_dictionary)
        elif cover_file_type == 'V':
            args_dictionary = {
                'input_file': path_to_cover_file(user_id, cover_file_name),
                'output_file': path_to_encoded_file(user_id, replace_file_extension(filename, 'avi')),
                'message_file': path_to_encoded_file(user_id, filename),
                'operation': 'encode',
                'user_id': user_id,
                'storage_id': storage_id,
            }
            video_commands.main(args_dictionary)
        print(args_dictionary)


def decode_file(user_id, storage_id, encoded_file, encode_file_type, encrypted_password, private_key, key_file):
    """
    Decrypts a file using AES decryption and a key that has been encrypted with
    RSA encryption. Saves the decrypted file to disk and updates the corresponding
    StorageDecode object with the path to the decrypted file.

    Args:
        userid (int): The ID of the user who owns the file.
        encoded_file (File): The file that has been encrypted with AES.
        encrypted_password (str): The key that has been encrypted with RSA.
        private_key (str): The private key to use for RSA decryption.
        storage_id (int): The ID of the corresponding StorageDecode object.
        encode_file_type (str): The type of the encoded file.
        key_file (File): The file that contains the key.

    Returns:
        None
    """

    print(user_id)
    print(storage_id)
    print(encoded_file)
    print(encrypted_password)
    print(private_key)
    print(encode_file_type)
    print(key_file)
    # filename = encoded_file.name.split('/')[-1]
    # print(filename)

    # file_in = open(path_to_encoded_file(userid, filename), "rb")
    # nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    # file_in.close()

    # key = rsa.decrypt(base64.b64decode(encrypted_password.encode('utf-8')),
    #                   rsa.PrivateKey.load_pkcs1(private_key))
    # cipher = AES.new(key, AES.MODE_EAX, nonce)
    # data = cipher.decrypt_and_verify(ciphertext, tag)
    # with open(path_to_decoded_file(userid, filename), 'wb') as f2:
    #     f2.write(data)
    #     StorageDecode.objects.filter(id=storage_id).update(
    #         decoded_file=path_to_decoded_file(userid, filename))
    if (encode_file_type == 'A'):
        args_dictionary = {
            'input_file': encoded_file,
            'key_file': key_file,
            'operation': 'decode',
            'user_id': user_id,
            'storage_id': storage_id,
            'encrypted_password': encrypted_password,
            'private_key': private_key
        }
        audio_commands.main(args_dictionary)
    elif (encode_file_type == 'I'):
        args_dictionary = {
            'input_file': encoded_file,
            'key_file': key_file,
            'operation': 'decode',
            'user_id': user_id,
            'storage_id': storage_id,
            'encrypted_password': encrypted_password,
            'private_key': private_key
        }
        image_commands.main(args_dictionary)
    elif (encode_file_type == 'V'):
        args_dictionary = {
            'input_file': encoded_file,
            'key_file': key_file,
            'operation': 'decode',
            'user_id': user_id,
            'storage_id': storage_id,
            'encrypted_password': encrypted_password,
            'private_key': private_key
        }
        video_commands.main(args_dictionary)


def replace_file_extension(file_name, extension):
    """Replace the extension of a file name

        Parameters:
          file_name: File name to change the extension
          extension: extension to change to

        Returns:
          Extension of the file as string

    """
    prefix, _, _ = file_name.rpartition('.')
    return prefix + '.' + extension

# def encrypt_file(hidded_file, pubkey, userid, privkey, storedPk):
#     filename = hidded_file.name.split('/')[-1]
#     print(filename)
#     pathtohiddedfile = os.path.join(
#         settings.MEDIA_ROOT, f"upload/{userid}/hidden_files/{filename}")
#     pathtoencodedfile = os.path.join(
#         settings.MEDIA_ROOT, f"upload/{userid}/encoded_files/{filename}")
#     pathtodecodedfile = os.path.join(
#         settings.MEDIA_ROOT, f"upload/{userid}/decoded_files/{filename}")
#     with open(pathtohiddedfile, 'rb') as f:
#         data = f.read()
#         key = get_random_bytes(16)
#         cipher = AES.new(key, AES.MODE_EAX)
#         ciphertext, tag = cipher.encrypt_and_digest(data)

#         file_out = open(pathtoencodedfile, "wb")
#         [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
#         file_out.close()

#         crypto = rsa.encrypt(key, rsa.PublicKey.load_pkcs1(pubkey))

#         file_in = open(pathtoencodedfile, "rb")
#         nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
#         file_in.close()

#         # let's assume that the key is somehow available again
#         key = rsa.decrypt(crypto, rsa.PrivateKey.load_pkcs1(privkey))
#         cipher = AES.new(key, AES.MODE_EAX, nonce)
#         data = cipher.decrypt_and_verify(ciphertext, tag)
#         # print(data)
#         with open(pathtodecodedfile, 'wb') as f2:
#             f2.write(data)
#             StorageEncode.objects.filter(id=storedPk).update(
#                 encoded_file=pathtoencodedfile)
