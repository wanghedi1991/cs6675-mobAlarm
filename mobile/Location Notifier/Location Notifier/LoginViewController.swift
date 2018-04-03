//
//  LoginViewController.swift
//  Location Notifier
//
//  Created by Hedi Wang on 3/24/18.
//  Copyright © 2018 Hedi Wang. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet weak var loginLabel: UILabel!
    @IBOutlet weak var usernameLabel: UILabel!
    @IBOutlet weak var usernameText: UITextField!
    
    @IBOutlet weak var passwordTextField: UITextField!
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        usernameText.delegate = self
        //self.navigationItem.titleView = UIImageView(image: UIImage(named: "title_small.png"))
        self.navigationItem.title = "Login Page"
        let loginItem = UIBarButtonItem(title: "Login", style: UIBarButtonItemStyle.plain, target: self, action: #selector(loginButtonPressed))
        
        self.navigationItem.rightBarButtonItem = loginItem
        self.navigationController?.navigationBar.tintColor = UIColor.white
    
        usernameText.leftViewMode = UITextFieldViewMode.always
        let imageView = UIImageView(frame: CGRect(x: 0, y: 0, width: 30, height: 30))
        let image = UIImage(named: "user.png")
        imageView.image = image
        usernameText.leftView = imageView
        
        passwordTextField.leftViewMode = UITextFieldViewMode.always
        let imageViewPassword = UIImageView(frame: CGRect(x: 0, y: 0, width: 30, height: 30))
        let imagePassword = UIImage(named: "password.png")
        imageViewPassword.image = imagePassword
        passwordTextField.leftView = imageViewPassword
        passwordTextField.delegate = self
    }

    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        usernameText.endEditing(true)
        return true
    }
    
    @IBAction func loginButtonPressed(_ sender: UIButton) {
        let storyBoard: UIStoryboard = UIStoryboard(name: "Main", bundle: nil)
        let newViewController = storyBoard.instantiateViewController(withIdentifier: "tableHolderController") as! TableHolderController
        self.navigationController?.pushViewController(newViewController, animated: true)
    }
    

}
