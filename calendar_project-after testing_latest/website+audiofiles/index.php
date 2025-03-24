<?php
require("./calendar/Audio_Manager/callbacks/config.php");
session_start();

// Prepare the SQL query to fetch the img_url where id = 1
$sql = "SELECT img_url FROM upload_image WHERE id = 1";
$result = $con->query($sql); // Execute the query

// Check if the query returned any rows
if ($result->num_rows > 0) {
    // Fetch the result as an associative array
    $image = $result->fetch_assoc();

    // Output the image with the src set to the img_url

} else {
    // If no image is found, display a placeholder or an alternative message
    echo '<img id="bag" src="path/to/placeholder-image.png" alt="No image available">';
}



$sql3 = "SELECT `id`, `v1`, `v2`, `v3`, `v4`, `v5` FROM `audio_details` WHERE 1";
$result = $con->query($sql3);

$data1 = [];
if ($result->num_rows > 0) {
    // Fetch each row and store it in an array
    while ($row1 = $result->fetch_assoc()) {
        // Other code...
        $v1 = $row1['v1'];
        $v2 = $row1['v2'];
        $v3 = $row1['v3'];
        $v4 = $row1['v4'];
        $v5 = $row1['v5'];
    }
}


$settings = '<button id="openSettings" class="settings-btn">Open Settings</button>';

$upload = '<form style="position:absolute;top:0;left:10px;" id="upload-form" enctype="multipart/form-data">

    <label style="display:inline-block;color:white;" for="bg-upload" class="bg-upload">Background  Image</label>  <br> 
    <input type="file" id="bg-upload" name="file" style="display:none;" accept="image/*">
    
    <center><button id="bg-btn" type="submit">Upload</button><span  id="file-name" style="margin-top: 10px; font-weight: bold;color:white;"></span></center>
</form>';

$login = '<button id="calendar-btn" class="login-btn" name="submit" type="submit">Login</button>';

$schedule = '<form action="./calendar/index.php" >
                <button id="login-btn" type="submit">Schedule</button>
            </form>';
$logout = ' <form action="./calendar/Audio_Manager/callbacks/logout.php">
    <button id="settings-btn">Logout</button>
    </form>';
?>



<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <link rel="stylesheet" href="./calendar/Audio_Manager/Assests/css/home.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <style>
        #bag {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            /* Ensures the image covers the entire area */
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            z-index: -1;
            /* Keep the background behind other content */
            margin: 0;
            padding: 0;
        }

        #upload-wrapper {
            margin: 20px;
        }


        /* Modal Background */
        .modal {
            display: none;
            /* Hidden by default */
            position: fixed;
            /* Stay in place */
            z-index: 1;
            /* Sit on top */
            left: 0;
            top: 0;
            width: 100%;
            /* Full width */
            height: 700px;
            /* Full height */
            overflow: auto;
            /* Enable scroll if needed */

        }

        /* Modal Content */
        .modal-content {
            position: relative;
            top: -150px;
            left: auto;
            /* Position it relative to the modal */
            background-color: #fefefe;
            /* White background */
            margin: auto;
            /* Center it */
            padding: 20px;
            /* Padding */
            border: 1px solid #888;
            /* Border */
            width: 90%;
            /* Width responsive */
            max-width: 500px;
            /* Max width */
            height: auto;
            /* Auto height */
            border-radius: 8px;
            /* Rounded corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            /* Shadow */
        }

        /* Close Button */

        /* Close button hover */


        /* Form Styles */
        form {
            display: flex;
            flex-direction: column;
            /* Stack inputs vertically */
        }

        /* Input Fields */
        input[type="text"] {
            margin-bottom: 5px;
            /* Space between inputs */
            padding: 10px;
            /* Padding */
            border: 1px solid #ccc;
            /* Border */
            border-radius: 4px;
            /* Rounded corners */
        }

        /* Update Button */
        /* Modal styles */
        .modal {
            display: none;
            /* Hidden by default */
            position: fixed;
            /* Stay in place */
            z-index: 1000;
            /* Sit on top */
            left: 0;
            top: 0;
            width: 100%;
            /* Full width */
            height: 100%;
            /* Full height */
            overflow: auto;
            /* Enable scroll if needed */
            background-color: rgba(245, 245, 245, 0.2);
            /* Black w/ opacity */
        }

        .modal-content {
            background-color: rgba(245, 245, 245, 1);
            /* Dark background */
            margin: 15% auto;
            /* 15% from the top and centered */
            padding: 20px;
            border: 1px solid #888;
            width: 400px;
            /* Width of the modal */
            color: white;
            /* Text color */
        }



        /* Button styles */
        .settings-btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            margin-top: -50px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 10px;
        }

        .settings-btn:hover {
            background-color: #45a049;
            /* Darker green */
        }

        /* Overlay styles */
        #overlay {
            position: fixed;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: none;
        z-index: 1;
        }

        /* Style for fieldset f1 with overlay and hover effect */
        #f1 {
            position: relative;
            overflow: hidden;
            /* Ensure overlay stays within f1 boundaries */
            background-image: url('your-background-image-url');
            /* Add your background image */
            background-size: cover;
            background-position: center;
            transition: all 0.3s ease-in-out;
            /* Smooth transition on hover */
        }




        /* To make sure the content within contan appears above the overlay */
    </style>
</head>

<body>



    <img id="bag" src="<?php echo htmlspecialchars($image['img_url']); ?>" alt="">






    <!-- Edit button -->


    <!-- Modal for editing -->


    <div id="grids"></div>

    <fieldset id="contan">
        <!-- Button to Open the Modal -->


        <div id="navbar">
            <?php

            if (isset($_SESSION["username"])) {
                echo $schedule;


                echo $logout;
            } else {
            }



            ?>

        </div>

        <?php
        if (isset($_SESSION["username"])) {
            if ($_SESSION["usertype"] == 0) {
                echo $settings;
            } else {
            }
        }

        if (!isset($_SESSION["username"])) {
            echo $login;
        }

        ?>


        <!-- Overlay for the modal -->
        

        <!-- Settings Modal -->
        <div id="settingsModal" class="modal">
            <div class="modal-content1">


                <h2 style="color:black;font-weight:bold;">Settings</h2><br>
                <fieldset>
                    <h4>Title Update </h4><br>
                    <button id="openModal" class="detail-btn">Update Title</button><br>
                    <hr>
                    <div style="margin-top: 10px;">
                        <h4>Background - Image</h4>
                        <form style="position:relative; margin-top: 20px;" id="upload-form" enctype="multipart/form-data">

                            <label style="display:flex; justify-content:space-around; color:white;" id="bg-label" for="bg-upload" class="bg-upload">Choose</label><br>
                            <input type="file" id="bg-upload" name="file" style="display:none;" accept="image/*">
                            <center>
                                <p id="file-name" style="font-weight: bold;margin-top:3px;"></p>
                                <button id="bg-btn" type="submit">Upload</button>
                                <button class="close" style="height: 43px;width:100px;background-color:red;padding:2px;" id="closeModal">Cancel</button>

                            </center>
                        </form>
                    </div>
                </fieldset>
            </div>
        </div>




        <!-- The Modal -->




        <!-- <fieldset id="f1">
            <button id="upload"><i class="fa-solid fa-file-arrow-up"></i></button>
        
            </fieldset>
   -->
        <fieldset id="f1">

            <input type="text" id="audio" placeholder="" readonly>
        </fieldset>


        <!-- Form to display Thirukkural details -->
        <fieldset id="f2">
            <h4 style="color:black;font-weight:bold; margin-bottom:5px;">Audio Details</h4>
            <hr>
            <form id="details">

                <label for="a"><?php echo $v1; ?></label>

                <input type="text" id="a" readonly>

                <label for="t"><?php echo $v2; ?></label>
                <input type="text" id="t" readonly>

                <label for="details"><?php echo $v3; ?></label>
                <textarea name="thirukural" id="detail" rows="10" cols="50" readonly></textarea>
            </form>

        </fieldset>

        <fieldset id="f3">
            <h4 style="color:black;font-weight:bold;"> Audio Control</h4>
            <hr>

            <form id="play1">
                <label for="aid"><?php echo $v4; ?></label>
                <input type="number" name="aid" id="aid">
                <center>
                    <h1>OR</h1>
                </center>
                <label for="tid"><?php echo $v5; ?></label>
                <input type="number" name="tid" id="tid">

                <div id="btn-control">
                    <div id="btn-group">

                        <button id="prev"><i class="fa-solid fa-backward fa-beat"></i></button>
                        <!-- Play/Pause Button -->

                        <button id="pause"><i class="fa-solid fa-pause fa-beat" style="color: #ffffff;"></i></button>
                        <a id="play" href="#" class="btn btn-primary">
                            <span id="icon" class="fa-solid fa-play fa-beat" style="color: #fbfefd;"></span>

                        </a>

                        <button id="stop"><i class="fa-solid fa-stop fa-beat" style="color: #ffffff;"></i></button>

                        <button id="next"><i class="fa-solid fa-forward fa-beat"></i></button>
                        <input type="hidden" id="aid" value="1" />
                        <input type="hidden" id="tid" value="1" />
                    </div>
                </div>

            </form>
        </fieldset>

    </fieldset>
    </div>

    </div>

    <!--     
    <div id="login-popup">
        <h2>Login</h2>
        <form action="./calendar/Audio_Manager/callbacks/login.php" method="post">
            <label for="username">Username</label>
            <input id="username" type="text" name="username" placeholder="Enter your username" required>
            <label for="password">Password</label>
            <input id="password" type="password" name="password" placeholder="Enter your password" required>

            <button type="submit" name="submit" class="submit-btn">Login</button>
        </form>
        <br>
        <form action="#">
            <button type="submit" class="cancel-btn">Cancel</button>
        </form>
    </div> -->




    <!-- Settings Panel -->

    <!-- Overlay background -->





    <!-- Modal Structure -->
    <div id="audioModal" class="modal">
        <div class="modal-content" style="width: 500px;height:675px; ">
            <h2>Update Form</h2>

            <form action="./calendar/Audio_Manager/callbacks/updatedetail.php" method="post" id="updateForm">
                <label id="i1" for="input1">Main Folder:</label>
                <input type="text" id="input1" name="input1" value="<?php echo $v1; ?>">

                <label id="i2" for="input2">Sub Folder:</label>
                <input type="text" id="input2" name="input2" value="<?php echo $v2; ?>">

                <label id="i3" for="input3">SubFolder 1:</label>
                <input type="text" id="input3" name="input3" value="<?php echo $v3; ?>">

                <label id="i4" for="input4">Adhigaram:</label>
                <input type="text" id="input4" name="input4" value="<?php echo $v4; ?>">

                <label id="i5" for="input5">Thirukkural:</label>
                <input type="text" id="input5" name="input5" value="<?php echo $v5; ?>">

                <button type="submit" style="margin-top:10px;">Update</button>
                <button type="button" style="background-color: red;margin-top:10px;" id="cancelButton">Cancel</button>

            </form>


        </div>
    </div>


    <div id="overlay"></div>
    <!-- Popup for Login Form -->
    <div id="login-popup">
        <h2>Login</h2>
        <form action="./calendar/Audio_Manager/callbacks/login.php" method="post">
            <label for="username">Username </label>
            <input id="username" type="text" name="username" placeholder="Enter your username" required>
            <label for="password">Password</label>
            <input id="password" type="password" name="password" placeholder="Enter your password" required>
            <button type="submit" name="submit" class="submit-btn">Login</button>

        </form>
        <form action="#">
            <button type="submit" id="cancel-btn" class="cancel-btn">Cancel</button>
        </form>
    </div>





    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

    <script>
       

       $(document).ready(function() {

          // Event listener for the cancel button
     
            // Toggle settings panel
            document.getElementById('settings-btn')?.addEventListener('click', function() {
                var panel = document.getElementById('settings-panel');
                panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
            });

            // Change button color
            document.getElementById('button-color')?.addEventListener('input', function() {
                var color = this.value;
                document.querySelectorAll('.button-row button, .center-button button, #calendar-btn').forEach(function(button) {
                    button.style.backgroundColor = color;
                });
            });

            // Change text color
            document.getElementById('text-color')?.addEventListener('input', function() {
                var color = this.value;
                document.querySelectorAll('#audio, legend, h1, .button-row button, .center-button button, #calendar-btn').forEach(function(element) {
                    element.style.color = color;
                });
            });

            // Dark mode toggle
            document.getElementById('dark-mode')?.addEventListener('change', function() {
                if (this.checked) {
                    document.body.style.backgroundColor = '#333';
                    document.body.style.color = '#f0f2f5';
                    document.querySelector('fieldset').style.backgroundColor = '#fff';
                    document.querySelector('fieldset').style.borderColor = '#555';
                    panel.style.color = "black";
                } else {
                    document.body.style.backgroundColor = '#f0f2f5';
                    document.body.style.color = '#333';
                    document.querySelector('fieldset').style.backgroundColor = '#fff';
                    document.querySelector('fieldset').style.borderColor = '#ccc';
                }
            });




const formData = new FormData();

formData.append('audio_running_status', 0); // 1 for running status
formData.append('audio_stop_status', 0); // 1 for stop status
formData.append('audio_pause_status', 0); // Reset pause status

sendAjaxRequest(formData);
function sendAjaxRequest(formData) {
        // First AJAX call to select.php (only when playing or stopping)
        $.ajax({
            url: './calendar/Audio_Manager/callbacks/initialize.php',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log("First Ajax call (select.php) successful");
            },
            error: function() {
                console.error('Error in first Ajax call');
            }
        })

    }
})


        



        $(document).ready(function() {

            const aidInput = document.getElementById('aid');
            const tidInput = document.getElementById('tid');
            const bag = document.getElementById("bag");
            // The OR text
            bag.addEventListener('click', function() {
                aidInput.style.display = 'block';
                tidInput.style.display = 'block'; // Hide tid input

                // Hide the OR text
            });

            // Function to hide the other input when one is focused
            aidInput.addEventListener('focus', function() {
                     
                tidInput.prop('disabled', true);  // Disable
 // Enable

              
                // Hide the OR text
            });

            tidInput.addEventListener('focus', function() {
                aidInput.prop('disabled', true);  // Disable
            
            });

            // Optionally, reset the visibility if the user clicks away
            aidInput.addEventListener('blur', function() {
                if (!tidInput.value) {
                    tidInput.style.display = 'inline'; // Show tid input again if it's empty
                    orText.style.display = 'block'; // Show the OR text again
                }
            });

            tidInput.addEventListener('blur', function() {
                if (!aidInput.value) {
                    aidInput.style.display = 'inline'; // Show aid input again if it's empty
                    orText.style.display = 'block'; // Show the OR text again
                }
            });












            document.getElementById('cancelButton').addEventListener('click', function() {
                document.getElementById('audioModal').style.display = 'none';
            });

            // Optionally, close the modal when clicking outside of it
            window.onclick = function(event) {
                if (event.target == document.getElementById('audioModal')) {
                    document.getElementById('audioModal').style.display = 'none';
                }
            };


            $('#openSettings').on('click', function() {
                $('#overlay').show();
                $('#settingsModal').css('display', 'block');
            });

            // Close modal
            $('#closeModal, #overlay').on('click', function() {
                $('#overlay').hide();
                $('#settingsModal').css('display', 'none');
            });

            // Show file name when selected
            $('#bg-upload').on('change', function() {
                const fileName = this.files[0] ? this.files[0].name : 'No file selected';
                $('#file-name').text(fileName); // Show the file name
            });


            // Event listener for the calendar button
            document.getElementById('calendar-btn')?.addEventListener('click', function() {
                document.getElementById('login-popup').style.display = 'block';
                document.getElementById('overlay').style.display = 'block';
            });
            
            document.getElementById('cancel-btn')?.addEventListener('click', function() {
                document.getElementById('login-popup').style.display = 'none';
                document.getElementById('overlay').style.display = 'none';
            });

            $("#upload").on("click", function() {
                $("#upload-popup").show();
                $("#overlay").show();
            });

            // Close popup when clicking cancel or overlay
            $(".ucancel-btn, #overlay").on("click", function() {
                $("#upload-popup").hide();
                $("#overlay").hide();
            });
            $(document).ready(function() {
                let currentTid = parseInt($("#tid").val()) || 1;
                let currentAid = parseInt($("#aid").val()) || 1;

                // Update initial values based on user input
                $("#tid").on('input', function() {
                    currentTid = parseInt($(this).val()) || 1;
                });

                $("#aid").on('input', function() {
                    currentAid = parseInt($(this).val()) || 1;
                });

                // Handle Play button
                $("#play").click(function(event) {
                    event.preventDefault();
                    handlePlay(); // Only Play will update select.php
                });

                // Handle Pause button
                $("#pause").click(function(event) {
                    event.preventDefault();
                    handlePause();
                });

                // Handle Next button
                $("#next").click(function(event) {
                    event.preventDefault();
                    handleNext(); // No select.php update
                });

                // Handle Previous button
                $("#prev").click(function(event) {
                    event.preventDefault();
                    handlePrev(); // No select.php update
                });

                // Handle Stop button
                $("#stop").click(function(event) {
                    event.preventDefault();
                    handleStop();
                });

                // Play Audio and update data
                function handlePlay() {
                    sendAudioRequest(1, 0); // 1 for playing status, 0 for pause status
                }

                // Pause Audio
                function handlePause() {
                    sendAudioRequest(1, 1); // 1 for running status, 1 for pause status
                }

                // Handle Next without sending data to select.php
                function handleNext() {
                    if ($("#tid").val()) {
                        currentTid++;
                        $("#tid").val(currentTid);
                    } else if ($("#aid").val()) {
                        currentAid++;
                        $("#aid").val(currentAid);
                    }
                    fetchData(); // Only fetch data from fetch.php
                }

                // Handle Previous without sending data to select.php
                function handlePrev() {
                    if ($("#tid").val() && currentTid > 1) {
                        currentTid--;
                        $("#tid").val(currentTid);
                    } else if ($("#aid").val() && currentAid > 1) {
                        currentAid--;
                        $("#aid").val(currentAid);
                    }
                    fetchData(); // Only fetch data from fetch.php
                }

                // Handle Stop
                function handleStop() {
                    const formData = new FormData();
                    const aidValue = $("#aid").val();
                    const tidValue = $("#tid").val();

                    if (aidValue && !tidValue) {
                        formData.append('aid', aidValue);
                    } else if (tidValue) {
                        formData.append('tid', tidValue);
                    } else {
                        console.error('Neither aid nor tid is provided');
                        return;
                    }

                    formData.append('audio_running_status', 1); // 1 for running status
                    formData.append('audio_stop_status', 1); // 1 for stop status
                    formData.append('audio_pause_status', 2); // Reset pause status

                    sendAjaxRequest(formData); // Send Stop request
                }

                // Fetch new data from fetch.php only
                function fetchData() {
                    const formData = new FormData();
                    const aidValue = $("#aid").val();
                    const tidValue = $("#tid").val();

                    if (aidValue && !tidValue) {
                        formData.append('aid', aidValue);
                    } else if (tidValue) {
                        formData.append('tid', tidValue);
                    } else {
                        console.error('Neither aid nor tid is provided');
                        return;
                    }

                    // Fetch only from fetch.php, no select.php call
                    $.ajax({
                        url: './calendar/Audio_Manager/callbacks/fetch.php',
                        type: 'POST',
                        data: formData,
                        contentType: false,
                        processData: false,
                        success: function(response) {
                            try {
                                const data = JSON.parse(response);
                                if (data.error) {
                                    alert('Error: ' + data.error);
                                } else if (Array.isArray(data) && data.length > 0) {
                                    let verses = data.map(detail =>
                                        `*${detail.Verse}*`
                                    );
                                    $('#a').val(data[0].ChapterName);
                                    $('#t').val(data[0].section);
                                    $('#detail').html(verses.join('\n\n')); // Update Thirukkural content
                                    console.log("Data fetched:", data);
                                } else {
                                    console.log('No data found');
                                }
                            } catch (e) {
                                console.error('Error parsing JSON response:', e);
                            }
                        },
                        error: function() {
                            console.error('Error in fetch data call');
                        }
                    });
                }

                // Send Audio Request (for Play/Pause)
                function sendAudioRequest(audioRunningStatus, audioPauseStatus) {
                    const formData = new FormData();
                    const aidValue = $("#aid").val();
                    const tidValue = $("#tid").val();

                    if (aidValue && !tidValue) {
                        formData.append('aid', aidValue);
                    } else if (tidValue) {
                        formData.append('tid', tidValue);
                    } else {
                        console.error('Neither aid nor tid is provided');
                        return;
                    }

                    formData.append('audio_running_status', audioRunningStatus); // 1 for play, 0 for stop
                    formData.append('audio_pause_status', audioPauseStatus); // 1 for pause, 0 for not paused
                    formData.append('audio_stop_status', 0); // Reset stop status

                    sendAjaxRequest(formData); // Send request to select.php and fetch.php
                }

                // Send AJAX Request to select.php and fetch.php
                function sendAjaxRequest(formData) {
                    // First AJAX call to select.php (only when playing or stopping)
                    $.ajax({
                        url: './calendar/Audio_Manager/callbacks/select.php',
                        type: 'POST',
                        data: formData,
                        contentType: false,
                        processData: false,
                        success: function(response) {
                            console.log("First Ajax call (select.php) successful");
                        },
                        error: function() {
                            console.error('Error in first Ajax call');
                        }
                    }).done(function() {
                        // Second AJAX call to fetch.php
                        $.ajax({
                            url: './calendar/Audio_Manager/callbacks/fetch.php',
                            type: 'POST',
                            data: formData,
                            contentType: false,
                            processData: false,
                            success: function(response) {
                                try {
                                    const data = JSON.parse(response);
                                    if (data.error) {
                                        alert('Error: ' + data.error);
                                    } else if (Array.isArray(data) && data.length > 0) {
                                        let verses = data.map(detail =>
                                            `*${detail.Verse}*`
                                        );
                                        $('#a').val(data[0].ChapterName);
                                        $('#t').val(data[0].section);
                                        $('#detail').html(verses); // Update Thirukkural content
                                        console.log("Data fetched:", data);
                                    } else {
                                        console.log('No data found');
                                    }
                                } catch (e) {
                                    console.error('Error parsing JSON response:', e);
                                }
                            },
                            error: function() {
                                console.error('Error in second Ajax call');
                            }
                        });
                    });
                }
            });


            $(document).ready(function() {
                // Fetch the latest image on page load
                fetchLatestImage();


                document.getElementById('bg-upload').addEventListener('change', function() {
                    const fileName = this.files[0] ? this.files[0].name : 'No file selected';
                    document.getElementById('file-name').textContent = fileName; // Show the file name
                });



                $('#upload-form').on('submit', function(event) {
                    event.preventDefault(); // Prevent the default form submission

                    // Initialize FormData
                    var formData = new FormData(this);

                    // AJAX request to upload the file
                    $.ajax({
                        url: './calendar/Audio_Manager/callbacks/upload.php', // Update with your PHP script path
                        type: 'POST',
                        data: formData,
                        processData: false, // Important: Don't process the data
                        contentType: false, // Important: Don't set content type
                        success: function(response) {
                            try {
                                var data = JSON.parse(response);

                                if (data.success) {
                                    // Update the src of the img tag to the newly uploaded image
                                    $('#bag').attr('src', data.img_url);
                                    document.getElementById('bg-upload').value = ''; // Clear the input
                                    document.getElementById('file-name').textContent = '';
                                    // Optionally fetch the latest image from the database
                                    fetchLatestImage();
                                } else {
                                    console.error("Upload failed:", data.error);
                                }
                            } catch (error) {
                                console.error("Error parsing JSON response:", error);
                            }
                        },
                        error: function(xhr, status, error) {
                            console.error(error);
                        }
                    });
                });

                function fetchLatestImage() {
                    $.ajax({
                        url: './calendar/Audio_Manager/callbacks/fetch_image.php', // Update with your PHP script path
                        type: 'GET',
                        success: function(response) {
                            try {
                                var data = JSON.parse(response);

                                if (data.img_url) {
                                    // Update the src of the img tag with the latest image URL
                                    $('#bag').attr('src', data.img_url);
                                }
                            } catch (error) {
                                console.error("Error parsing JSON response:", error);
                            }
                        },
                        error: function(xhr, status, error) {
                            console.error(error);
                        }
                    });
                }
            });




            

            // Get the modal
            var modal = document.getElementById("audioModal");

            // Get the button that opens the modal
            var btn = document.getElementById("openModal");

            // Get the <span> element that closes the modal
            var span = document.getElementsByClassName("close");

            // When the user clicks the button, open the modal 
            btn.onclick = function() {
                modal.style.display = "block";
            }

            // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
            }

            // When the user clicks anywhere outside of the modal, close it
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }




            // Function to update time
            function updateTime() {
                const now = new Date();
                const options = {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: 'numeric',
                    minute: 'numeric',
                    second: 'numeric',
                    hour12: true
                };
                const dateString = now.toLocaleString('en-US', options);
                document.getElementById('audio').value = dateString;
            }

            // Update the time immediately and every second
            updateTime();
            setInterval(updateTime, 1000);
        });
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/js/all.min.js"></script>

    <!-- <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script> -->

</body>

</html>