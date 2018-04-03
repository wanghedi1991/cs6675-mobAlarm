//
//  RegisterViewController.swift
//  Location Notifier
//
//  Created by Hedi Wang on 4/2/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit

class RegisterViewController: UIViewController, UITextFieldDelegate {


    @IBOutlet weak var usernameText: UITextField!
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        usernameText.delegate = self
        self.navigationItem.title = "Register"
        let registerItem = UIBarButtonItem(title: "Register", style: UIBarButtonItemStyle.plain, target: self, action: #selector(registerButtonPressed))
        registerItem.tintColor = UIColor.white
        
        self.navigationItem.rightBarButtonItem = registerItem
        self.navigationController?.navigationBar.tintColor = UIColor.white
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        usernameText.endEditing(true)
        return true
    }

    @IBAction func registerButtonPressed(_ sender: UIButton) {
        self.navigationController?.popViewController(animated: true)
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
