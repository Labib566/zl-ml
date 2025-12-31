const { ethers } = require("hardhat");
const fs = require("fs"); // ফাইল সিস্টেম লাইব্রেরি যোগ করা হয়েছে
const path = require("path"); // পাথ ম্যানেজমেন্টের জন্য

async function main() {
  const Verifier = await ethers.getContractFactory("Groth16Verifier");
  const verifier = await Verifier.deploy();
  await verifier.waitForDeployment();   // ✅ ethers v6

  const ZKML = await ethers.getContractFactory("ZKMLVerifier");
  const zkml = await ZKML.deploy(await verifier.getAddress());
  await zkml.waitForDeployment();        // ✅ ethers v6

  const verifierAddress = await verifier.getAddress();
  const zkmlAddress = await zkml.getAddress();

  console.log("Verifier:", verifierAddress);
  console.log("ZKML:", zkmlAddress);

  // --- ফাইল সেভ করার নতুন কোড শুরু ---
  const addressData = {
    verifier: verifierAddress,
    zkml: zkmlAddress,
    timestamp: new Date().toISOString()
  };

  // আপনার api/zk ফোল্ডারের ভেতরে deployed_address.json ফাইলটি তৈরি হবে
  const filePath = path.join(__dirname, "../../api/zk/deployed_address.json");

  // writeFileSync আগের সব ডেটা মুছে নতুন করে ফাইল লিখে (Overwrite)
  fs.writeFileSync(filePath, JSON.stringify(addressData, null, 2));
  console.log("✅ New addresses saved to api/zk/deployed_address.json");
  // --- ফাইল সেভ করার কোড শেষ ---
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });