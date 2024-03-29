import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { AiFillSafetyCertificate } from "react-icons/ai";
import { FaMapMarkedAlt } from "react-icons/fa";
import { RiExchangeDollarLine, RiLineChartLine, RiAdminLine } from "react-icons/ri";
import { BiLogOut } from "react-icons/bi";
import { HiUsers } from "react-icons/hi";
import { FaPowerOff, FaTruck } from "react-icons/fa";
import "./Navbar.css";

const Navbar = () => {
  const [isMinimazed, setIsMinimazed] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="navbar">
      <div className="nav-logo"></div>
      <div className="sidebar-main">
        <div
          className="sidebar-item"
          onClick={() => {
            navigate("/overview");
          }}
        >
          <FaMapMarkedAlt />
          <div className="sidebar-title">Overview</div>
        </div>
        <div
          className="sidebar-item"
          onClick={() => {
            navigate("/assets?view=0");
          }}
        >
          <FaTruck />
          <div className="sidebar-title">Assets</div>
        </div>
        <div
          className="sidebar-item"
          onClick={() => {
            navigate("/users");
          }}
        >
          <HiUsers />
          <div className="sidebar-title">Users</div>
        </div>
        <div
          className="sidebar-item"
          onClick={() => {
            navigate("/safety?view=0");
          }}
        >
          <AiFillSafetyCertificate />
          <div className="sidebar-title">Safety</div>
        </div>
        <div className="sidebar-item">
          <RiExchangeDollarLine />
          <div className="sidebar-title">Accounting</div>
        </div>
      </div>
      <div className="sidebar-settings">
        <div
          className="sidebar-item"
          onClick={() => {
            navigate("/logout");
          }}
        >
          <FaPowerOff />
          <div className="sidebar-title">Logout</div>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
