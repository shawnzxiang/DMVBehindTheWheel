<?PHP

$to = '5301234567@txt.att.net'; // This example is for att that I used. Text message telnumber@server. Go to "http://20somethingfinance.com/how-to-send-text-messages-sms-via-email-for-free/" for all service providers
    $email_subject = "DMV appointment found!";
    $email_body = "Go to https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do";
    $headers = "From: noreply@email.com\n"; 
    $headers .= "Reply-To:noreply@email.com";
    mail($to,$email_subject,$email_body,$headers);

?>
