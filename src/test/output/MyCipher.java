package ir.ac.kntu;

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class MyCipher {

    private static final MyCipher instance = new MyCipher();

    private final HashMap<String, ArrayList<String>> map;
	private final String mainKeyHex = "8b280f156d4c1bffc77f9365f9c18081";

	private final String mainIvHex = "de158dcb698288efda30d8a3ffe69b93";

	private MyCipher(){
		map = new HashMap<>();
		map.put(
		"736aabc3c0c6dff117c1b2949ccabebe"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));//number reader.nextInt() 
 		map.put(
		"4c6aa4d28bc799f03fdca8a8badff8f3dc76e2b08f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));//choice Menu.shoMenuHandler() 
 		map.put(
		"4461bec2d79490bf1cccabbf97ccacb7"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"5860bf87c0da85fa00"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"6063a3"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"6063a3e7c2d990f61e97a5b29f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"303df9"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"6c62ae"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"6c62aee7c2d990f61e97a5b29f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"353afc"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"6c6abece"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"6c6abecee5d39cfe1bd5e8be9dd3"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"757dbfc2"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"31"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"303f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"333f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"323f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"353f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"343f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
 		map.put(
		"5163afc6d6d1d1fc1ad6a9ae979ef7b799478527e3555339484f"
		,new ArrayList<>(Arrays.asList(
		"8b280f156d4c1bffc77f9365f9c18081","de158dcb698288efda30d8a3ffe69b93")));// 
     }

    public static MyCipher getInstance() {
        return instance;
    }

    private ArrayList<String> findFromHex(String hex) throws NullPointerException{
        for (Map.Entry<String, ArrayList<String>> set :
                this.map.entrySet()) {
            if (set.getKey().equals(hex)){
                return set.getValue();
            }
        }
        //TODO  check for double encoding
        return new ArrayList<String>();
    }

    public String decode(String ciphertextHex) {
        try {

            String keyHex = this.mainKeyHex;
            String ivHex = this.mainIvHex;
            byte[] iv = hexStringToByteArray(ivHex);
            byte[] keyBytes = hexStringToByteArray(keyHex);

            // Create a SecretKeySpec from the key
            SecretKeySpec keySpec = new SecretKeySpec(keyBytes, "AES");

            // Create an AES cipher with CFB mode
            Cipher cipher = Cipher.getInstance("AES/CFB/NoPadding");
            cipher.init(Cipher.DECRYPT_MODE, keySpec, new IvParameterSpec(iv));

            // Convert hex ciphertext to byte array
            byte[] ciphertext = hexStringToByteArray(ciphertextHex);

            // Decrypt the ciphertext
            byte[] decryptedBytes = cipher.doFinal(ciphertext);

            // Convert the decrypted bytes to a string
            return new String(decryptedBytes);
        } catch (Exception e) {
            //System.out.println("Error in decoding");
            return "Error";
        }

    }

    public String encode(Object o) {
        String value = o.toString();
        String keyHex = this.mainKeyHex;
        String inputString = value;
        // Convert the hexadecimal key to bytes
        byte[] key = hexStringToByteArray(keyHex);
        byte[] iv = hexStringToByteArray(mainIvHex);
        try {
            // Create an AES cipher with the key and IV
            Cipher cipher = Cipher.getInstance("AES/CFB/NoPadding");
            SecretKeySpec secretKeySpec = new SecretKeySpec(key, "AES");
            IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
            cipher.init(Cipher.ENCRYPT_MODE, secretKeySpec, ivParameterSpec);

            // Encrypt the input string
            byte[] ciphertext = cipher.doFinal(inputString.getBytes(StandardCharsets.UTF_8));
            String ivHex = byteArrayToHexString(iv);
            String ciphertextHex = byteArrayToHexString(ciphertext);
            ArrayList<String> tmpArray = new ArrayList<>();
            tmpArray.add(keyHex);
            tmpArray.add(ivHex);
            this.map.put(ciphertextHex,tmpArray);
            return ciphertextHex;
        } catch (Exception e){
            //System.out.println("Error in decoding");
            return "Error";
        }
    }

    private byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i + 1), 16));
        }
        return data;
    }

    private static String generateRandomHexKey() {
        SecureRandom random = new SecureRandom();
        byte[] key = new byte[16];
        random.nextBytes(key);
        return byteArrayToHexString(key);
    }

    private static byte[] generateRandomIV() {
        SecureRandom random = new SecureRandom();
        byte[] iv = new byte[16];
        random.nextBytes(iv);
        return iv;
    }

    private static String byteArrayToHexString(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }


}