<?php
$to 			= 'sales@powerdata2go.com';
$subject 		= "Enquiry form Power Data 2Go"  . $_REQUEST['heroFname'];
$name 			= $_REQUEST['heroFname'];
$lname          = $_REQUEST['heroLname'];
$email 			= $_REQUEST['heroEmail'];
$phone 			= $_REQUEST['phone'];
$message 		= $_REQUEST['message'];

$msg			='
					<table>
						<tr>
							<td>Name</td><td>"'.$name.''.$lname.'"</td>
						</tr>
						<tr>
							<td>Email</td><td>"'.$email.'"</td>
						</tr>
						<tr>
							<td>Phone</td><td>"'.$phone.'"</td>
						</tr>
						
						<tr>
							<td>Message</td><td>"'.$message.'"</td>
						</tr>
					</table>
';

$headers .= "FROM: $email";
$headers = 
        "MIME-Version: 1.0\r\n" .
        "Content-Type: text/html; charset=UTF-8\r\n";


//$headers .= "MIME-Version: 1.0" . "\r\n";
//$headers .= "Content-type:text/html;charset=UTF-8" . "\r\n";


$send = mail( $to, $subject, $msg, $headers);
         
         if( $send == true )
         {
            header("Location:thank-you.php");
            //echo "<script>alert('Message sent successfully...');</script>";
            
         }
         else
         {
           header("Location:index.php");
           //echo "<script>alert('Message could not be sent...);</script>";
           
         }
?>
