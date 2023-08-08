pragma solidity 0.8.19;

interface IMevShareCaptureLogger {
    function winnerCaptures (address, uint) external view returns (bool);
}

contract Checker {
    IMevShareCaptureLogger public logger = IMevShareCaptureLogger(0x6C9c151642C0bA512DE540bd007AFa70BE2f1312);
    address public me = 0x846603628D071EcD09b876D842a809DF2A93309B;

    function checker() public view {
        require(logger.winnerCaptures(me, 203)==true);
    }
}